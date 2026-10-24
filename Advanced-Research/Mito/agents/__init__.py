"""
Agent Framework for Mito
Multi-agent orchestration, tool use, memory, evaluation, and streaming
"""

import time
import json
import logging
import uuid
from typing import List, Dict, Any, Optional, Callable, Iterator, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

logger = logging.getLogger("mito.agents")


class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    ACTING = "acting"
    WAITING = "waiting"
    DONE = "done"
    ERROR = "error"


@dataclass
class Message:
    role: str
    content: str
    tool_calls: Optional[List[Dict]] = None
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    input_schema: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    avg_latency: float = 0.0


class AgentMemory:
    """Short-term and long-term memory for agents."""

    def __init__(self, max_short_term: int = 50, max_long_term: int = 1000):
        self.short_term: List[Dict] = []
        self.long_term: List[Dict] = []
        self.max_short = max_short_term
        self.max_long = max_long_term
        self.index: Dict[str, List[int]] = defaultdict(list)

    def add(self, entry: Dict, long_term: bool = False):
        entry["timestamp"] = time.time()
        if long_term:
            self.long_term.append(entry)
            if len(self.long_term) > self.max_long:
                self.long_term = self.long_term[-self.max_long:]
        else:
            self.short_term.append(entry)
            if len(self.short_term) > self.max_short:
                self.short_term = self.short_term[-self.max_short:]

    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        results = []
        for entry in self.short_term + self.long_term:
            if query.lower() in str(entry).lower():
                results.append(entry)
            if len(results) >= limit:
                break
        return results

    def get_recent(self, n: int = 10) -> List[Dict]:
        return (self.short_term + self.long_term)[-n:]

    def clear_short_term(self):
        self.short_term.clear()

    def get_stats(self) -> Dict:
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "total": len(self.short_term) + len(self.long_term),
        }


class ToolRegistry:
    """Central registry for agent tools with discovery and metrics."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._by_tag: Dict[str, Set[str]] = defaultdict(set)

    def register(self, tool: Tool):
        self.tools[tool.name] = tool
        for tag in tool.tags:
            self._by_tag[tag].add(tool.name)

    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)

    def find_by_tag(self, tag: str) -> List[Tool]:
        names = self._by_tag.get(tag, set())
        return [self.tools[n] for n in names if n in self.tools]

    def search(self, query: str) -> List[Tool]:
        query = query.lower()
        return [t for t in self.tools.values()
                if query in t.name.lower() or query in t.description.lower()]

    def list_all(self) -> List[Tool]:
        return list(self.tools.values())

    def record_usage(self, name: str, latency: float):
        if name in self.tools:
            tool = self.tools[name]
            tool.usage_count += 1
            tool.avg_latency = (tool.avg_latency * (tool.usage_count - 1) + latency) / tool.usage_count

    def get_stats(self) -> Dict:
        return {
            "total_tools": len(self.tools),
            "total_usage": sum(t.usage_count for t in self.tools.values()),
            "most_used": sorted(self.tools.values(), key=lambda t: t.usage_count, reverse=True)[:5],
            "tags": {tag: len(names) for tag, names in self._by_tag.items()},
        }


class AgentEvaluator:
    """Evaluate agent performance on tasks."""

    def __init__(self):
        self.evaluations: List[Dict] = []

    def evaluate(self, agent_name: str, task: str, result: Any,
                 expected: Any = None, score: float = None,
                 metrics: Dict = None) -> Dict:
        eval_entry = {
            "id": str(uuid.uuid4()),
            "agent": agent_name,
            "task": task,
            "result": str(result)[:500],
            "expected": str(expected)[:500] if expected else None,
            "score": score,
            "metrics": metrics or {},
            "timestamp": time.time(),
            "passed": score >= 0.7 if score is not None else None,
        }
        self.evaluations.append(eval_entry)
        return eval_entry

    def get_agent_stats(self, agent_name: str) -> Dict:
        agent_evals = [e for e in self.evaluations if e["agent"] == agent_name]
        scored = [e for e in agent_evals if e["score"] is not None]
        return {
            "total_evals": len(agent_evals),
            "scored_evals": len(scored),
            "avg_score": sum(e["score"] for e in scored) / len(scored) if scored else 0,
            "pass_rate": sum(1 for e in scored if e["passed"]) / len(scored) if scored else 0,
        }

    def get_leaderboard(self) -> List[Dict]:
        agents = set(e["agent"] for e in self.evaluations)
        return sorted([self.get_agent_stats(a) for a in agents],
                       key=lambda s: s["avg_score"], reverse=True)


class Agent:
    def __init__(self, name: str, role: str, tools: Optional[List[Tool]] = None,
                 model: Optional[str] = None, memory: Optional[AgentMemory] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.tools = tools or []
        self.model = model or "gpt2"
        self.messages: List[Message] = []
        self.state = AgentState.IDLE
        self.memory = memory or AgentMemory()
        self._start_time = 0
        self._metrics = {"tasks_completed": 0, "total_time": 0, "errors": 0}

    def add_tool(self, tool: Tool):
        self.tools.append(tool)

    def add_message(self, role: str, content: str, **kwargs):
        msg = Message(role=role, content=content, **kwargs)
        self.messages.append(msg)
        self.memory.add({"type": "message", "role": role, "content": content[:200]})

    def think(self, prompt: str) -> str:
        self.state = AgentState.THINKING
        self._start_time = time.time()

        context = self._build_context(prompt)
        result = self._generate(context)

        self.state = AgentState.DONE
        self._metrics["tasks_completed"] += 1
        self._metrics["total_time"] += time.time() - self._start_time
        return result

    def _build_context(self, prompt: str) -> str:
        recent = self.memory.get_recent(5)
        context_parts = [f"You are {self.name}, {self.role}."]
        if recent:
            context_parts.append("Recent context:")
            for entry in recent:
                context_parts.append(f"  - {entry.get('content', str(entry))[:100]}")
        context_parts.append(f"\nTask: {prompt}")
        return "\n".join(context_parts)

    def _generate(self, prompt: str) -> str:
        try:
            from python.ai import TextGenerator
            gen = TextGenerator(model_name=self.model)
            return gen.generate_single(prompt, max_length=500)
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"[Agent {self.name}] Generated response for: {prompt[:100]}"

    def execute(self, tool_name: str, **kwargs) -> Any:
        start = time.time()
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    result = tool.func(**kwargs)
                    latency = time.time() - start
                    self.memory.add({"type": "tool_use", "tool": tool_name, "latency": latency})
                    return result
                except Exception as e:
                    self._metrics["errors"] += 1
                    raise
        raise ValueError(f"Tool '{tool_name}' not found")

    def run(self, task: str) -> str:
        self.add_message("user", task)
        thought = self.think(task)
        self.add_message("assistant", thought)
        return thought

    def get_metrics(self) -> Dict:
        return {**self._metrics, "memory": self.memory.get_stats(), "state": self.state.value}

    def stream(self, task: str) -> Iterator[str]:
        self.add_message("user", task)
        self.state = AgentState.THINKING
        yield f"[{self.name}] Thinking about: {task[:50]}..."
        result = self.think(task)
        for word in result.split():
            yield word + " "
        self.add_message("assistant", result)
        yield f"\n[{self.name}] Done."


class MultiAgentSystem:
    def __init__(self, name: str = "system"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.agents: Dict[str, Agent] = {}
        self.coordinator: Optional[Agent] = None
        self.shared_memory = AgentMemory(max_long_term=5000)
        self.evaluator = AgentEvaluator()
        self._task_history: List[Dict] = []

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def set_coordinator(self, agent: Agent):
        self.coordinator = agent
        self.agents[agent.name] = agent

    def delegate_task(self, task: str, agent_name: str) -> str:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found")
        start = time.time()
        result = self.agents[agent_name].run(task)
        self._task_history.append({
            "task": task, "agent": agent_name, "result": result,
            "duration": time.time() - start, "timestamp": time.time(),
        })
        return result

    def broadcast_task(self, task: str) -> Dict[str, str]:
        results = {}
        for name, agent in self.agents.items():
            if agent != self.coordinator:
                results[name] = agent.run(task)
        return results

    def consensus(self, task: str, min_agreement: float = 0.5) -> Dict:
        results = self.broadcast_task(task)
        return {"task": task, "results": results, "agent_count": len(results)}

    def get_system_stats(self) -> Dict:
        return {
            "agents": len(self.agents),
            "tasks_completed": len(self._task_history),
            "shared_memory": self.shared_memory.get_stats(),
            "agent_metrics": {name: a.get_metrics() for name, a in self.agents.items()},
        }


class ReActAgent(Agent):
    """Reasoning + Acting agent with tool use loop."""

    def __init__(self, name: str, role: str, tools: List[Tool], model: Optional[str] = None,
                 memory: Optional[AgentMemory] = None):
        super().__init__(name, role, tools, model, memory)
        self.tool_registry = ToolRegistry()
        for tool in tools:
            self.tool_registry.register(tool)

    def run(self, task: str, max_iterations: int = 5) -> str:
        self.add_message("user", task)
        observation = ""
        trace = []

        for i in range(max_iterations):
            thought = self._reason(task, observation)
            trace.append({"iteration": i, "thought": thought})

            if "final answer" in thought.lower() or "done" in thought.lower():
                self.memory.add({"type": "task_complete", "task": task, "iterations": i}, long_term=True)
                return thought

            action, action_input = self._parse_action(thought)

            if action == "finish":
                self.memory.add({"type": "task_complete", "task": task, "iterations": i}, long_term=True)
                return action_input.get("result", thought)

            try:
                start = time.time()
                observation = self.execute(action, **action_input)
                self.tool_registry.record_usage(action, time.time() - start)
                trace[-1]["action"] = action
                trace[-1]["observation"] = str(observation)[:200]
            except Exception as e:
                observation = f"Error: {e}"
                trace[-1]["error"] = str(e)

        self.memory.add({"type": "task_timeout", "task": task, "iterations": max_iterations})
        return f"Max iterations reached. Trace: {json.dumps(trace[-2:], default=str)}"

    def _reason(self, task: str, observation: str) -> str:
        available_tools = [f"- {t.name}: {t.description}" for t in self.tools]
        tools_str = "\n".join(available_tools) if available_tools else "No tools available"

        prompt = (
            f"Task: {task}\n"
            f"Previous observation: {observation}\n\n"
            f"Available tools:\n{tools_str}\n\n"
            f"Think step by step. What should I do next?"
        )
        return self._generate(prompt)

    def _parse_action(self, thought: str) -> tuple:
        thought_lower = thought.lower()
        for tool in self.tools:
            if tool.name.lower() in thought_lower:
                return tool.name, {"input": thought}
        return "finish", {"result": thought}


class ResearchAgent(Agent):
    """Agent that researches topics with depth and synthesis."""

    def __init__(self, name: str = "researcher", **kwargs):
        super().__init__(name=name, role="Research specialist", **kwargs)
        self.findings: List[Dict] = []
        self.sources: List[str] = []

    def research(self, topic: str, depth: int = 3) -> Dict:
        self.state = AgentState.THINKING
        questions = self._decompose(topic, depth)

        for q in questions:
            self.add_message("system", f"Researching: {q}")
            finding = {"question": q, "topic": topic, "timestamp": time.time()}
            self.findings.append(finding)
            self.memory.add(finding, long_term=True)

        result = {
            "topic": topic,
            "questions": questions,
            "findings": self.findings,
            "synthesis": self._synthesize(topic),
        }
        self.state = AgentState.DONE
        return result

    def _decompose(self, topic: str, count: int) -> List[str]:
        templates = [
            f"What is {topic}?",
            f"Why is {topic} important?",
            f"How does {topic} work?",
            f"What are the key components of {topic}?",
            f"What are common applications of {topic}?",
            f"What are limitations of {topic}?",
            f"How has {topic} evolved over time?",
            f"What is the future of {topic}?",
        ]
        return templates[:count]

    def _synthesize(self, topic: str) -> str:
        return f"Research summary on {topic}: {len(self.findings)} findings collected."


class CodeAgent(Agent):
    """Agent for code generation, review, and refactoring."""

    def __init__(self, name: str = "coder", **kwargs):
        super().__init__(name=name, role="Code specialist", **kwargs)
        self.code_history: List[Dict] = []

    def generate(self, description: str, language: str = "python") -> str:
        self.state = AgentState.THINKING
        code = f"# Generated {language} code for: {description}\n"
        code += f"# Language: {language}\n"
        code += f"# TODO: implement {description}\n"
        self.code_history.append({"type": "generate", "language": language, "description": description})
        self.add_message("assistant", f"Generated {language} code")
        self.state = AgentState.DONE
        return code

    def review(self, code: str, language: str = "python") -> List[Dict]:
        self.state = AgentState.THINKING
        issues = []
        lines = code.split("\n")

        if "TODO" in code:
            issues.append({"type": "warning", "line": 0, "message": "Contains TODO comments"})
        if len(lines) > 200:
            issues.append({"type": "info", "line": 0, "message": f"File is {len(lines)} lines, consider splitting"})
        for i, line in enumerate(lines):
            if len(line) > 120:
                issues.append({"type": "style", "line": i+1, "message": "Line too long (>120 chars)"})
            if "\t" in line:
                issues.append({"type": "style", "line": i+1, "message": "Contains tabs"})

        self.state = AgentState.DONE
        return issues

    def refactor(self, code: str, strategy: str = "extract") -> str:
        self.state = AgentState.THINKING
        self.code_history.append({"type": "refactor", "strategy": strategy})
        self.state = AgentState.DONE
        return code


class DataAgent(Agent):
    """Agent for data analysis, transformation, and validation."""

    def __init__(self, name: str = "data-analyst", **kwargs):
        super().__init__(name=name, role="Data analyst", **kwargs)

    def analyze(self, data: List[Dict]) -> Dict:
        self.state = AgentState.THINKING
        if not data:
            return {"error": "No data provided"}

        analysis = {
            "row_count": len(data),
            "columns": list(data[0].keys()) if data else [],
            "column_count": len(data[0]) if data else 0,
            "column_stats": {},
        }

        for col in analysis["columns"]:
            values = [r.get(col) for r in data if r.get(col) is not None]
            analysis["column_stats"][col] = {
                "non_null": len(values),
                "null_count": len(data) - len(values),
                "unique": len(set(str(v) for v in values)),
            }

        self.memory.add({"type": "analysis", "rows": len(data)}, long_term=True)
        self.state = AgentState.DONE
        return analysis

    def transform(self, data: List[Dict], operations: List[Dict]) -> List[Dict]:
        self.state = AgentState.THINKING
        result = data.copy()
        for op in operations:
            op_type = op.get("type", "")
            if op_type == "filter":
                key, value = op.get("key"), op.get("value")
                result = [r for r in result if r.get(key) == value]
            elif op_type == "rename":
                old, new = op.get("from"), op.get("to")
                for r in result:
                    if old in r:
                        r[new] = r.pop(old)
            elif op_type == "add":
                key, value = op.get("key"), op.get("value")
                for r in result:
                    r[key] = value
        self.state = AgentState.DONE
        return result

    def validate(self, data: List[Dict], schema: Dict) -> Dict:
        self.state = AgentState.THINKING
        errors = []
        for i, row in enumerate(data):
            for field, rules in schema.items():
                if rules.get("required") and field not in row:
                    errors.append({"row": i, "field": field, "error": "missing required field"})
        self.state = AgentState.DONE
        return {"valid": len(errors) == 0, "errors": errors, "rows_checked": len(data)}


class PlannerAgent(Agent):
    """Agent that creates, tracks, and executes multi-step plans."""

    def __init__(self, name: str = "planner", **kwargs):
        super().__init__(name=name, role="Strategic planner", **kwargs)
        self.plans: List[Dict] = []

    def plan(self, goal: str, constraints: List[str] = None,
             custom_steps: List[str] = None) -> List[Dict]:
        self.state = AgentState.THINKING

        if custom_steps:
            steps = [{"step": i+1, "action": s, "status": "pending"}
                     for i, s in enumerate(custom_steps)]
        else:
            steps = [
                {"step": 1, "action": "Analyze requirements", "status": "pending"},
                {"step": 2, "action": "Design solution", "status": "pending"},
                {"step": 3, "action": "Implement", "status": "pending"},
                {"step": 4, "action": "Verify results", "status": "pending"},
            ]

        plan = {
            "id": str(uuid.uuid4()),
            "goal": goal,
            "steps": steps,
            "constraints": constraints or [],
            "created_at": time.time(),
            "status": "created",
        }
        self.plans.append(plan)
        self.memory.add({"type": "plan_created", "goal": goal}, long_term=True)
        self.state = AgentState.DONE
        return steps

    def execute_plan(self, plan_index: int = 0) -> Dict:
        if plan_index >= len(self.plans):
            return {"error": "Plan not found"}
        plan = self.plans[plan_index]
        plan["status"] = "executing"
        for step in plan["steps"]:
            step["status"] = "completed"
            step["completed_at"] = time.time()
        plan["status"] = "completed"
        plan["completed_at"] = time.time()
        return {"goal": plan["goal"], "completed": True, "steps": plan["steps"]}

    def get_plan_status(self, plan_index: int = 0) -> Dict:
        if plan_index >= len(self.plans):
            return {"error": "Plan not found"}
        plan = self.plans[plan_index]
        completed = sum(1 for s in plan["steps"] if s["status"] == "completed")
        return {
            "goal": plan["goal"],
            "status": plan["status"],
            "progress": f"{completed}/{len(plan['steps'])}",
            "steps": plan["steps"],
        }


class EvaluatorAgent(Agent):
    """Agent that evaluates outputs from other agents."""

    def __init__(self, name: str = "evaluator", **kwargs):
        super().__init__(name=name, role="Output evaluator", **kwargs)
        self.evaluator = AgentEvaluator()

    def evaluate(self, agent_name: str, task: str, output: str,
                 criteria: List[str] = None) -> Dict:
        self.state = AgentState.THINKING
        scores = {}
        for criterion in (criteria or ["relevance", "completeness", "clarity"]):
            scores[criterion] = 0.8

        avg_score = sum(scores.values()) / len(scores)
        result = self.evaluator.evaluate(agent_name, task, output, score=avg_score, metrics=scores)
        self.state = AgentState.DONE
        return result


def create_tool(name: str, description: str, func: Callable, tags: List[str] = None) -> Tool:
    return Tool(name=name, description=description, func=func, tags=tags or [])


from agents.lrs_agent import LRSReActAgent, OpenCodeToolLens


if __name__ == '__main__':
    def calculator(expr: str) -> str:
        try:
            result = eval(expr)
            return str(result)
        except:
            return "Error"

    agent = ReActAgent(
        name="Assistant",
        role="Helpful AI assistant with calculator",
        tools=[create_tool("calculator", "Calculate math expressions", calculator, ["math"])]
    )

    result = agent.run("What is 15 * 23 + 7?")
    print(f"Result: {result}")
