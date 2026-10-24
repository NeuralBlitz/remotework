"""
Mito Workflow Engine
DAG-based workflow execution with retries, branching, parallel steps
"""

import json
import logging
import time
import uuid
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger("mito.workflow")


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


@dataclass
class StepConfig:
    name: str
    func: Callable
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    retries: int = 0
    retry_delay: float = 1.0
    timeout: float = 0
    condition: Optional[Callable] = None
    on_failure: Optional[str] = None  # step name to run on failure
    tags: List[str] = field(default_factory=list)


@dataclass
class StepResult:
    step_name: str
    status: StepStatus
    result: Any = None
    error: str = ""
    start_time: float = 0
    end_time: float = 0
    attempts: int = 1


@dataclass
class WorkflowResult:
    workflow_id: str
    status: WorkflowStatus
    step_results: Dict[str, StepResult]
    start_time: float
    end_time: float
    error: str = ""


class WorkflowStep:
    def __init__(self, config: StepConfig):
        self.config = config
        self.status = StepStatus.PENDING
        self.result: Any = None
        self.error: str = ""
        self.attempts = 0

    def execute(self, context: Dict[str, Any]) -> Any:
        if self.config.condition and not self.config.condition(context):
            self.status = StepStatus.SKIPPED
            return None

        self.status = StepStatus.RUNNING
        last_error = None

        for attempt in range(1, self.config.retries + 2):
            self.attempts = attempt
            try:
                if self.config.timeout > 0:
                    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FETimeout
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(
                            self.config.func,
                            *self.config.args,
                            context=context,
                            **self.config.kwargs,
                        )
                        self.result = future.result(timeout=self.config.timeout)
                else:
                    self.result = self.config.func(
                        *self.config.args, context=context, **self.config.kwargs
                    )

                self.status = StepStatus.SUCCESS
                return self.result
            except Exception as e:
                last_error = e
                self.error = str(e)
                if attempt <= self.config.retries:
                    self.status = StepStatus.RETRYING
                    logger.warning(f"Step '{self.config.name}' attempt {attempt} failed: {e}")
                    time.sleep(self.config.retry_delay * attempt)
                else:
                    self.status = StepStatus.FAILED
                    logger.error(f"Step '{self.config.name}' failed after {attempt} attempts: {e}")

        raise last_error


class Workflow:
    def __init__(self, name: str, description: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.steps: Dict[str, WorkflowStep] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.reverse_deps: Dict[str, Set[str]] = {}
        self.context: Dict[str, Any] = {}

    def add_step(self, config: StepConfig) -> "Workflow":
        step = WorkflowStep(config)
        self.steps[config.name] = step
        self.dependencies[config.name] = set(config.depends_on)
        self.reverse_deps[config.name] = set()

        for dep in config.depends_on:
            if dep not in self.reverse_deps:
                self.reverse_deps[dep] = set()
            self.reverse_deps[dep].add(config.name)

        return self

    def set_context(self, key: str, value: Any):
        self.context[key] = value

    def get_execution_order(self) -> List[List[str]]:
        remaining = set(self.steps.keys())
        completed = set()
        layers = []

        while remaining:
            ready = {s for s in remaining if self.dependencies[s] <= completed}
            if not ready:
                raise ValueError(f"Circular dependency or missing step: {remaining}")
            layers.append(list(ready))
            completed.update(ready)
            remaining -= ready

        return layers

    def execute(self, context: Dict[str, Any] = None, max_workers: int = 4,
                on_step: Callable = None) -> WorkflowResult:
        ctx = {**self.context, **(context or {})}
        step_results: Dict[str, StepResult] = {}
        start_time = time.time()

        try:
            layers = self.get_execution_order()
        except ValueError as e:
            return WorkflowResult(
                workflow_id=self.id,
                status=WorkflowStatus.FAILED,
                step_results={},
                start_time=start_time,
                end_time=time.time(),
                error=str(e),
            )

        for layer in layers:
            parallel_steps = [s for s in layer if self.steps[s].status == StepStatus.PENDING]

            if len(parallel_steps) == 1:
                step_name = parallel_steps[0]
                step = self.steps[step_name]
                step_start = time.time()
                try:
                    result = step.execute(ctx)
                    ctx[step_name] = result
                    step_results[step_name] = StepResult(
                        step_name=step_name,
                        status=StepStatus.SUCCESS,
                        result=result,
                        start_time=step_start,
                        end_time=time.time(),
                        attempts=step.attempts,
                    )
                    if on_step:
                        on_step(step_name, step_results[step_name])
                except Exception as e:
                    step_results[step_name] = StepResult(
                        step_name=step_name,
                        status=StepStatus.FAILED,
                        error=str(e),
                        start_time=step_start,
                        end_time=time.time(),
                        attempts=step.attempts,
                    )
                    if on_step:
                        on_step(step_name, step_results[step_name])

                    if step.config.on_failure:
                        self._run_failure_handler(step.config.on_failure, ctx, step_results)

                    return WorkflowResult(
                        workflow_id=self.id,
                        status=WorkflowStatus.FAILED,
                        step_results=step_results,
                        start_time=start_time,
                        end_time=time.time(),
                        error=f"Step '{step_name}' failed: {e}",
                    )
            else:
                with ThreadPoolExecutor(max_workers=min(max_workers, len(parallel_steps))) as executor:
                    futures = {}
                    for step_name in parallel_steps:
                        step = self.steps[step_name]
                        step.status = StepStatus.RUNNING
                        step_start = time.time()
                        futures[executor.submit(step.execute, ctx)] = (step_name, step_start)

                    for future in as_completed(futures):
                        step_name, step_start = futures[future]
                        try:
                            result = future.result()
                            ctx[step_name] = result
                            step_results[step_name] = StepResult(
                                step_name=step_name,
                                status=StepStatus.SUCCESS,
                                result=result,
                                start_time=step_start,
                                end_time=time.time(),
                                attempts=self.steps[step_name].attempts,
                            )
                            if on_step:
                                on_step(step_name, step_results[step_name])
                        except Exception as e:
                            step_results[step_name] = StepResult(
                                step_name=step_name,
                                status=StepStatus.FAILED,
                                error=str(e),
                                start_time=step_start,
                                end_time=time.time(),
                                attempts=self.steps[step_name].attempts,
                            )
                            if on_step:
                                on_step(step_name, step_results[step_name])
                            return WorkflowResult(
                                workflow_id=self.id,
                                status=WorkflowStatus.FAILED,
                                step_results=step_results,
                                start_time=start_time,
                                end_time=time.time(),
                                error=f"Step '{step_name}' failed: {e}",
                            )

        return WorkflowResult(
            workflow_id=self.id,
            status=WorkflowStatus.SUCCESS,
            step_results=step_results,
            start_time=start_time,
            end_time=time.time(),
        )

    def _run_failure_handler(self, handler_name: str, context: Dict, step_results: Dict):
        if handler_name in self.steps:
            try:
                self.steps[handler_name].execute(context)
            except Exception as e:
                logger.error(f"Failure handler '{handler_name}' also failed: {e}")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": list(self.steps.keys()),
            "dependencies": {k: list(v) for k, v in self.dependencies.items()},
        }


class WorkflowBuilder:
    """Fluent builder for workflows."""

    def __init__(self, name: str, description: str = ""):
        self.workflow = Workflow(name, description)

    def step(self, name: str, func: Callable, depends_on: List[str] = None,
             retries: int = 0, timeout: float = 0, **kwargs) -> "WorkflowBuilder":
        config = StepConfig(
            name=name,
            func=func,
            depends_on=depends_on or [],
            retries=retries,
            timeout=timeout,
            **kwargs,
        )
        self.workflow.add_step(config)
        return self

    def parallel(self, steps: List[Dict]) -> "WorkflowBuilder":
        for step_cfg in steps:
            config = StepConfig(**step_cfg)
            self.workflow.add_step(config)
        return self

    def build(self) -> Workflow:
        return self.workflow
