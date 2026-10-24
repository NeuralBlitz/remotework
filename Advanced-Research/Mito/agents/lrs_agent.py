"""
LRS-ReAct Agent: ReActAgent enhanced with Active Inference via lrs-agents.
Provides precision tracking, free energy-based policy selection, and automatic
tool adaptation when failures occur.
"""

import time
import json
import logging
import uuid
from typing import List, Dict, Any, Optional, Callable, TYPE_CHECKING

try:
    from lrs.core.precision import PrecisionParameters, HierarchicalPrecision
    from lrs.core.lens import ToolLens, ExecutionResult
    from lrs.core.free_energy import (
        calculate_expected_free_energy,
        precision_weighted_selection,
    )
    LRS_AVAILABLE = True
except ImportError:
    LRS_AVAILABLE = False
    ToolLens = object
    ExecutionResult = object
    PrecisionParameters = object
    HierarchicalPrecision = object

from agents import (
    ReActAgent,
    Tool,
    AgentMemory,
    Message,
    AgentState,
)

logger = logging.getLogger("mito.lrs_agent")


class OpenCodeToolLens(ToolLens if LRS_AVAILABLE else object):
    """Wraps an opencode Tool as an LRS ToolLens for precision tracking."""

    def __init__(self, tool: Tool):
        if not LRS_AVAILABLE:
            raise ImportError("lrs-agents is not installed. Run: pip install lrs-agents")

        super().__init__(
            name=tool.name,
            input_schema=tool.input_schema or {},
            output_schema={},
        )
        self._tool = tool
        self._func = tool.func

    def get(self, state: Dict[str, Any]) -> ExecutionResult:
        start = time.time()
        try:
            kwargs = {}
            if "input" in state:
                kwargs["input"] = state["input"]
            elif "params" in state:
                kwargs = state["params"]
            elif state:
                kwargs = {k: v for k, v in state.items()
                          if k not in ("type", "timestamp")}

            result = self._func(**kwargs)
            latency = time.time() - start
            self._tool.usage_count += 1
            self._tool.avg_latency = (
                self._tool.avg_latency * (self._tool.usage_count - 1) + latency
            ) / self._tool.usage_count

            return ExecutionResult(
                success=True,
                value={"result": result, "latency": latency},
                error=None,
                prediction_error=0.1,
            )
        except Exception as e:
            self._tool.usage_count += 1
            return ExecutionResult(
                success=False,
                value=None,
                error=str(e),
                prediction_error=0.9,
            )

    def set(self, state: Dict[str, Any], obs: Any) -> Dict[str, Any]:
        return {**state, f"{self.name}_result": obs}


class LRSReActAgent(ReActAgent):
    """
    ReActAgent enhanced with Active Inference for automatic resilience.

    Key enhancements over ReActAgent:
    - Precision tracking via Beta-distributed confidence (gamma)
    - Free energy (G) based policy selection instead of heuristic parsing
    - Automatic tool adaptation when precision drops below threshold
    - Three-level hierarchical precision: execution -> planning -> abstract
    - Multi-proposal generation with precision-weighted selection

    The agent loop:
        1. Generate N policy proposals via LLM
        2. Evaluate Expected Free Energy for each: G = Epistemic - Pragmatic
        3. Select policy via softmax on precision-weighted G: P(pi) ~ exp(-gamma * G)
        4. Execute selected policy (tool call)
        5. Update precision from prediction error
        6. If precision < threshold: adaptation triggers, explore alternatives
    """

    def __init__(
        self,
        name: str,
        role: str,
        tools: List[Tool],
        model: Optional[str] = None,
        memory: Optional[AgentMemory] = None,
        num_proposals: int = 5,
        precision_threshold: float = 0.4,
        adaptation_enabled: bool = True,
        use_hierarchy: bool = True,
        preferences: Optional[Dict[str, float]] = None,
    ):
        super().__init__(name, role, tools, model, memory)

        if not LRS_AVAILABLE:
            raise ImportError(
                "lrs-agents is required. Install with: pip install lrs-agents"
            )

        self.num_proposals = num_proposals
        self.precision_threshold = precision_threshold
        self.adaptation_enabled = adaptation_enabled
        self.preferences = preferences or {"success": 5.0, "error": -3.0}

        self.precision = HierarchicalPrecision() if use_hierarchy else PrecisionParameters(
            alpha=1.0, beta=1.0, adaptation_threshold=precision_threshold
        )

        self._lrs_tool_registry = None
        self._tool_lenses: Dict[str, OpenCodeToolLens] = {}
        self._proposals: List[Dict] = []
        self._selected_policy: Optional[Dict] = None
        self._adaptation_count = 0
        self._precision_history: List[Dict] = []
        self._failed_tools: Dict[str, float] = {}

        for tool in tools:
            self._register_tool_lens(tool)

    def _register_tool_lens(self, tool: Tool):
        lens = OpenCodeToolLens(tool)
        self._tool_lenses[tool.name] = lens

    def _get_lrs_registry(self):
        if self._lrs_tool_registry is None:
            from lrs.core.registry import ToolRegistry
            self._lrs_tool_registry = ToolRegistry()
            for lens in self._tool_lenses.values():
                self._lrs_tool_registry.register(lens)
        return self._lrs_tool_registry

    def _generate_proposals(self, task: str, observation: str) -> List[Dict]:
        """Generate N diverse policy proposals via the LLM."""
        available_tools = [f"- {t.name}: {t.description}" for t in self.tools]
        tools_str = "\n".join(available_tools) if available_tools else "No tools available."

        gamma = self.precision.execution if hasattr(self.precision, 'execution') else self.precision.value
        strategy = "explore new approaches" if gamma < self.precision_threshold else "exploit known solutions"

        prompt = (
            f"You are an AI agent. Task: {task}\n"
            f"Previous result: {observation}\n\n"
            f"Available tools:\n{tools_str}\n\n"
            f"Generate exactly {self.num_proposals} different approaches to solve this.\n"
            f"For each approach, provide:\n"
            f"  1. A brief reasoning (2 sentences)\n"
            f"  2. The tool name to use\n"
            f"  3. Estimated success probability (0.0-1.0)\n"
            f"  4. Estimated info gain if it fails (0.0-2.0)\n"
            f"  5. Failure modes to watch for\n\n"
            f"Current strategy: {strategy} (precision={gamma:.2f})\n"
            f"Format as JSON array of objects with keys: reasoning, tool, success_prob, info_gain, failure_modes"
        )

        result = self._generate(prompt)
        try:
            proposals = json.loads(result)
            if not isinstance(proposals, list):
                proposals = self._parse_proposals_from_text(result)
        except (json.JSONDecodeError, TypeError):
            proposals = self._parse_proposals_from_text(result)

        for p in proposals:
            p.setdefault("reasoning", "No reasoning provided")
            p.setdefault("success_prob", 0.5)
            p.setdefault("info_gain", 1.0)
            p.setdefault("failure_modes", [])

        return proposals[: self.num_proposals]

    def _parse_proposals_from_text(self, text: str) -> List[Dict]:
        proposals = []
        for tool in self.tools:
            if tool.name.lower() in text.lower():
                proposals.append({
                    "reasoning": f"Use {tool.name} as suggested by the model.",
                    "tool": tool.name,
                    "success_prob": 0.5,
                    "info_gain": 1.0,
                    "failure_modes": ["tool unavailable", "wrong parameters"],
                })
        if not proposals:
            proposals.append({
                "reasoning": "No specific tool identified; return final answer.",
                "tool": "finish",
                "success_prob": 0.5,
                "info_gain": 0.0,
                "failure_modes": [],
            })
        return proposals

    def _evaluate_proposals(self, proposals: List[Dict], task: str) -> List[Dict]:
        """Evaluate proposals using Expected Free Energy G."""
        gamma = self.precision.execution if hasattr(self.precision, 'execution') else self.precision.value
        evaluated = []

        for proposal in proposals:
            tool_name = proposal.get("tool", "finish")
            success_prob = proposal.get("success_prob", 0.5)
            info_gain = proposal.get("info_gain", 1.0)

            if tool_name == "finish":
                pragmatic = success_prob * self.preferences.get("success", 5.0)
                epistemic = 0.0
                total_g = -pragmatic
            else:
                pragmatic = success_prob * self.preferences.get("success", 5.0)
                failure_penalty = (1 - success_prob) * abs(self.preferences.get("error", -3.0))
                epistemic = info_gain * (1 - gamma)

                tool_lens = self._tool_lenses.get(tool_name)
                if tool_lens:
                    failure_penalty += tool_lens.failure_count * 0.5

                total_g = epistemic - pragmatic + failure_penalty

            evaluated.append({
                **proposal,
                "g_value": total_g,
                "precision": gamma,
                "epistemic": epistemic,
                "pragmatic": pragmatic,
            })

        evaluated.sort(key=lambda x: x["g_value"])
        return evaluated

    def _select_policy(self, evaluated: List[Dict]) -> Dict:
        """Select policy via precision-weighted softmax on G values."""
        gamma = self.precision.execution if hasattr(self.precision, 'execution') else self.precision.value
        beta = 1.0

        g_values = [p["g_value"] for p in evaluated]
        weights = [float("inf") if g == float("-inf") else -beta * gamma * g for g in g_values]
        max_w = max(weights)
        exp_weights = [__import__("math").exp(w - max_w) for w in weights]
        total = sum(exp_weights)
        probs = [w / total for w in exp_weights]

        idx = max(range(len(probs)), key=lambda i: probs[i])
        return evaluated[idx]

    def _calculate_prediction_error(self, success: bool, tool_name: str) -> float:
        """Derive prediction error from execution outcome."""
        if success:
            return 0.1

        tool_lens = self._tool_lenses.get(tool_name)
        if tool_lens:
            base_error = 0.9
            repetition_penalty = min(tool_lens.failure_count * 0.05, 0.2)
            return min(base_error + repetition_penalty, 0.99)

        return 0.9

    def _record_precision_event(self, level: str, old_val: float, new_val: float, reason: str):
        """Record precision change to history and emit event."""
        self._precision_history.append({
            "timestamp": time.time(),
            "level": level,
            "old_precision": old_val,
            "new_precision": new_val,
            "reason": reason,
        })

        try:
            from events import Event, get_event_bus
            bus = get_event_bus()
            bus.emit(Event.create(
                "lrs.precision_update",
                data={
                    "agent_id": self.id,
                    "agent_name": self.name,
                    "level": level,
                    "old_precision": old_val,
                    "new_precision": new_val,
                    "reason": reason,
                    "adaptation_count": self._adaptation_count,
                },
                source="lrs_agent",
            ))
        except Exception:
            pass

    def _emit_tool_event(self, tool_name: str, success: bool, prediction_error: float,
                         latency: float, proposal: Dict):
        """Emit tool execution event to the event bus."""
        try:
            from events import Event, get_event_bus
            bus = get_event_bus()
            bus.emit(Event.create(
                "lrs.tool_execution",
                data={
                    "agent_id": self.id,
                    "agent_name": self.name,
                    "tool_name": tool_name,
                    "success": success,
                    "prediction_error": prediction_error,
                    "latency": latency,
                    "proposal_g": proposal.get("g_value"),
                    "precision": proposal.get("precision"),
                },
                source="lrs_agent",
            ))
        except Exception:
            pass

    def _emit_adaptation_event(self, old_precision: float, new_precision: float,
                               trigger: str, alternatives_found: int):
        """Emit adaptation event to the event bus."""
        self._adaptation_count += 1
        try:
            from events import Event, get_event_bus
            bus = get_event_bus()
            bus.emit(Event.create(
                "lrs.adaptation",
                data={
                    "agent_id": self.id,
                    "agent_name": self.name,
                    "level": "execution",
                    "old_precision": old_precision,
                    "new_precision": new_precision,
                    "trigger": trigger,
                    "alternatives_found": alternatives_found,
                    "adaptation_count": self._adaptation_count,
                },
                source="lrs_agent",
                priority=2,
            ))
        except Exception:
            pass

    def run(self, task: str, max_iterations: int = 5) -> str:
        """
        Run the LRS-enhanced ReAct loop.

        Extends ReActAgent.run() with:
        - Multi-proposal generation and free energy evaluation
        - Precision-weighted policy selection
        - Automatic adaptation on failure
        - Hierarchical precision updates
        - Structured event emission
        """
        self.add_message("user", task)
        observation = ""
        trace = []

        for i in range(max_iterations):
            gamma_before = (
                self.precision.execution if hasattr(self.precision, "execution")
                else self.precision.value
            )

            proposals = self._generate_proposals(task, observation)
            evaluated = self._evaluate_proposals(proposals, task)
            selected = self._select_policy(evaluated)
            self._selected_policy = selected
            self._proposals = evaluated

            tool_name = selected.get("tool", "finish")
            reasoning = selected.get("reasoning", "")

            trace.append({
                "iteration": i,
                "precision": gamma_before,
                "proposals_generated": len(proposals),
                "selected_tool": tool_name,
                "selected_g": selected.get("g_value"),
                "reasoning": reasoning[:100],
            })

            if tool_name == "finish":
                self._update_precision_after_execution(True, "finish", 0.1)
                self.memory.add({"type": "task_complete", "task": task, "iterations": i}, long_term=True)
                return f"{reasoning}\n\nFinal answer: {observation}"

            start = time.time()
            try:
                observation = self.execute(tool_name, **{"input": observation})
                latency = time.time() - start

                prediction_error = self._calculate_prediction_error(True, tool_name)
                self._update_precision_after_execution(True, tool_name, prediction_error)
                self._emit_tool_event(tool_name, True, prediction_error, latency, selected)

                trace[-1]["observation"] = str(observation)[:200]
                trace[-1]["success"] = True

            except Exception as e:
                latency = time.time() - start
                error_msg = str(e)
                observation = f"Error: {error_msg}"

                prediction_error = self._calculate_prediction_error(False, tool_name)
                self._update_precision_after_execution(False, tool_name, prediction_error)
                self._emit_tool_event(tool_name, False, prediction_error, latency, selected)

                trace[-1]["error"] = error_msg
                trace[-1]["success"] = False

                if self.adaptation_enabled:
                    gamma_after = (
                        self.precision.execution if hasattr(self.precision, "execution")
                        else self.precision.value
                    )
                    if self.precision.should_adapt() if hasattr(self.precision, "should_adapt") else (gamma_after < self.precision_threshold):
                        alternatives = self._find_alternative_tools(tool_name)
                        self._emit_adaptation_event(
                            old_precision=gamma_before,
                            new_precision=gamma_after,
                            trigger="precision_threshold",
                            alternatives_found=len(alternatives),
                        )
                        if alternatives:
                            observation = f"[LRS: Adapting] Previous tool '{tool_name}' failed (precision dropped to {gamma_after:.2f}). Trying alternative: {alternatives[0]}"

        self.memory.add({"type": "task_timeout", "task": task, "iterations": max_iterations})
        return f"Max iterations reached. Trace: {json.dumps(trace[-3:], default=str)}"

    def _update_precision_after_execution(self, success: bool, tool_name: str, prediction_error: float):
        """Update hierarchical precision based on execution outcome."""
        if hasattr(self.precision, "update"):
            old_execution = self.precision.execution if hasattr(self.precision, "execution") else self.precision.value

            self.precision.update("execution", prediction_error)

            if hasattr(self.precision, "propagation_threshold"):
                self.precision.update("planning", prediction_error * 0.7)
                self.precision.update("abstract", prediction_error * 0.4)

            new_execution = self.precision.execution if hasattr(self.precision, "execution") else self.precision.value

            self._record_precision_event(
                "execution", old_execution, new_execution,
                f"{'success' if success else 'failure'}: {tool_name}"
            )

            self._failed_tools[tool_name] = self._failed_tools.get(tool_name, 0) + (0 if success else 1)
        else:
            old = self.precision.value
            self.precision.update(prediction_error)
            self._record_precision_event(
                "global", old, self.precision.value,
                f"{'success' if success else 'failure'}: {tool_name}"
            )

    def _find_alternative_tools(self, failed_tool: str) -> List[str]:
        """Find alternative tools that haven't failed recently."""
        alternatives = []
        for tool_name, lens in self._tool_lenses.items():
            if tool_name == failed_tool:
                continue
            if lens.failure_count < 2:
                alternatives.append(tool_name)

        alternatives.sort(key=lambda t: self._failed_tools.get(t, 0))
        return alternatives

    def get_lrs_metrics(self) -> Dict[str, Any]:
        """Return LRS-specific metrics including precision trajectory."""
        precision_values = {}
        if hasattr(self.precision, "get_all_values"):
            precision_values = self.precision.get_all_values()
        elif hasattr(self.precision, "value"):
            precision_values = {"precision": self.precision.value}

        return {
            "lrs_version": "0.2.1" if LRS_AVAILABLE else "unavailable",
            "lrs_available": LRS_AVAILABLE,
            "precision": precision_values,
            "adaptation_count": self._adaptation_count,
            "precision_history": self._precision_history[-20:],
            "proposals_generated": len(self._proposals),
            "selected_policy": {
                "tool": self._selected_policy.get("tool") if self._selected_policy else None,
                "g_value": self._selected_policy.get("g_value") if self._selected_policy else None,
            },
            "failed_tools": dict(self._failed_tools),
            "tool_lens_stats": {
                name: {
                    "call_count": lens.call_count,
                    "failure_count": lens.failure_count,
                    "success_rate": lens.success_rate,
                }
                for name, lens in self._tool_lenses.items()
            },
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Return combined opencode + LRS metrics."""
        base = super().get_metrics()
        lrs = self.get_lrs_metrics()
        return {**base, **lrs}

    def get_policy_trajectory(self) -> List[Dict]:
        """Return the history of policy proposals and selections."""
        return self._proposals


if __name__ == "__main__":
    def calculator(expr: str) -> str:
        try:
            return str(eval(expr))
        except Exception as e:
            raise ValueError(f"Calculation error: {e}")

    agent = LRSReActAgent(
        name="LRS-Assistant",
        role="AI assistant with resilient calculator",
        tools=[
            Tool(
                name="calculator",
                description="Calculate math expressions",
                func=calculator,
                input_schema={"type": "object", "properties": {"expr": {"type": "string"}}},
                tags=["math"],
            )
        ],
    )

    result = agent.run("What is 15 * 23 + 7?")
    print(f"Result: {result}")
    print(f"Metrics: {json.dumps(agent.get_lrs_metrics(), indent=2)}")
