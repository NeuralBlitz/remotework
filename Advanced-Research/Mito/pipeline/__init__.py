"""
Pipeline System for Mito
Chain multiple AI operations together
"""

from typing import List, Dict, Any, Callable, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json



class PipelineStepType(Enum):
    PROMPT = "prompt"
    GENERATE = "generate"
    TRANSFORM = "transform"
    FILTER = "filter"
    AGGREGATE = "aggregate"
    CONDITIONAL = "conditional"
    BRANCH = "branch"


@dataclass
class PipelineStep:
    name: str
    step_type: PipelineStepType
    func: Optional[Callable] = None
    config: Dict[str, Any] = field(default_factory=dict)
    input_key: str = "input"
    output_key: str = "output"


@dataclass
class PipelineResult:
    success: bool
    data: Any
    steps_executed: List[str]
    errors: List[str] = field(default_factory=list)


class Pipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []
        self.variables: Dict[str, Any] = {}
    
    def add_step(self, step: PipelineStep):
        self.steps.append(step)
        return self
    
    def set_variable(self, key: str, value: Any):
        self.variables[key] = value
    
    def get_variable(self, key: str) -> Any:
        return self.variables.get(key)
    
    def execute(self, initial_input: Any) -> PipelineResult:
        context = {
            "input": initial_input,
            "variables": self.variables,
            "step_outputs": {}
        }
        errors = []
        executed = []
        
        for step in self.steps:
            try:
                result = self._execute_step(step, context)
                context["step_outputs"][step.name] = result
                context[step.output_key] = result
                executed.append(step.name)
            except Exception as e:
                errors.append(f"{step.name}: {str(e)}")
                return PipelineResult(
                    success=False,
                    data=context.get("output"),
                    steps_executed=executed,
                    errors=errors
                )
        
        return PipelineResult(
            success=True,
            data=context.get("output"),
            steps_executed=executed,
            errors=[]
        )
    
    def _execute_step(self, step: PipelineStep, context: Dict) -> Any:
        if step.step_type == PipelineStepType.PROMPT:
            return self._prompt_step(step, context)
        elif step.step_type == PipelineStepType.GENERATE:
            return self._generate_step(step, context)
        elif step.step_type == PipelineStepType.TRANSFORM:
            return self._transform_step(step, context)
        elif step.step_type == PipelineStepType.FILTER:
            return self._filter_step(step, context)
        elif step.step_type == PipelineStepType.AGGREGATE:
            return self._aggregate_step(step, context)
        elif step.step_type == PipelineStepType.CONDITIONAL:
            return self._conditional_step(step, context)
        return context.get(step.input_key)
    
    def _prompt_step(self, step: PipelineStep, context: Dict) -> str:
        template = step.config.get("template", "{input}")
        return template.format(input=context.get("input", ""))
    
    def _generate_step(self, step: PipelineStep, context: Dict) -> str:
        from python.ai import TextGenerator
        gen = TextGenerator(model_name=step.config.get("model", "gpt2"))
        return gen.generate_single(
            context.get(step.input_key, ""),
            max_length=step.config.get("max_tokens", 100)
        )
    
    def _transform_step(self, step: PipelineStep, context: Dict) -> Any:
        if step.func:
            return step.func(context.get(step.input_key))
        return context.get(step.input_key)
    
    def _filter_step(self, step: PipelineStep, context: Dict) -> List[Any]:
        items = context.get(step.input_key, [])
        if not isinstance(items, list):
            items = [items]
        
        filter_func = step.config.get("filter_func")
        if filter_func:
            return [item for item in items if filter_func(item)]
        
        condition = step.config.get("condition")
        if condition:
            return [item for item in items if item.get(condition.get("key")) == condition.get("value")]
        
        return items
    
    def _aggregate_step(self, step: PipelineStep, context: Dict) -> Any:
        items = context.get(step.input_key, [])
        operation = step.config.get("operation", "join")
        
        if operation == "join":
            separator = step.config.get("separator", " ")
            return separator.join(str(item) for item in items)
        elif operation == "sum":
            return sum(items)
        elif operation == "count":
            return len(items)
        elif operation == "first":
            return items[0] if items else None
        elif operation == "last":
            return items[-1] if items else None
        
        return items
    
    def _conditional_step(self, step: PipelineStep, context: Dict) -> Any:
        condition = step.config.get("condition")
        if_true = step.config.get("if_true")
        if_false = step.config.get("if_false")
        
        input_val = context.get(step.input_key)
        
        if callable(condition):
            result = condition(input_val)
        else:
            result = input_val == condition
        
        return if_true if result else if_false
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "steps": [
                {
                    "name": s.name,
                    "type": s.step_type.value,
                    "config": s.config
                }
                for s in self.steps
            ],
            "variables": self.variables
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Pipeline":
        pipeline = cls(data["name"])
        for step_data in data.get("steps", []):
            step = PipelineStep(
                name=step_data["name"],
                step_type=PipelineStepType(step_data["type"]),
                config=step_data.get("config", {})
            )
            pipeline.add_step(step)
        return pipeline


class Chain:
    """Simple chain for sequential processing"""
    
    def __init__(self):
        self.processors: List[Callable] = []
    
    def add(self, func: Callable) -> "Chain":
        self.processors.append(func)
        return self
    
    def execute(self, input_data: Any) -> Any:
        result = input_data
        for processor in self.processors:
            result = processor(result)
        return result
    
    def __call__(self, input_data: Any) -> Any:
        return self.execute(input_data)


class Parallel:
    """Run steps in parallel"""
    
    def __init__(self):
        self.tasks: List[Callable] = []
    
    def add(self, func: Callable, *args, **kwargs) -> "Parallel":
        self.tasks.append((func, args, kwargs))
        return self
    
    def execute(self) -> List[Any]:
        from concurrent.futures import ThreadPoolExecutor
        
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(func, *args, **kwargs)
                for func, args, kwargs in self.tasks
            ]
            results = [f.result() for f in futures]
        
        return results


def create_text_pipeline(
    name: str,
    prompt_template: str,
    model: str = "gpt2",
    max_tokens: int = 100
) -> Pipeline:
    """Quick text processing pipeline"""
    pipeline = Pipeline(name)
    
    pipeline.add_step(PipelineStep(
        name="format",
        step_type=PipelineStepType.PROMPT,
        config={"template": prompt_template}
    ))
    
    pipeline.add_step(PipelineStep(
        name="generate",
        step_type=PipelineStepType.GENERATE,
        config={"model": model, "max_tokens": max_tokens}
    ))
    
    return pipeline


def create_rag_pipeline(
    query: str,
    documents: List[str],
    top_k: int = 3
) -> Pipeline:
    """RAG pipeline"""
    from agents.rag import RAG, Document
    
    pipeline = Pipeline("rag")
    
    def retrieve(doc_list, q):
        from agents.rag import RAG
        r = RAG(llm_model="gpt2")
        r.add_documents(doc_list)
        return r.query(q)
    
    pipeline.add_step(PipelineStep(
        name="retrieve",
        step_type=PipelineStepType.TRANSFORM,
        func=lambda x: retrieve(documents, query),
        output_key="context"
    ))
    
    return pipeline


if __name__ == '__main__':
    pipe = create_text_pipeline("test", "Summarize: {input}", max_tokens=50)
    result = pipe.execute("The quick brown fox jumps over the lazy dog.")
    print(f"Success: {result.success}")
    print(f"Output: {result.data}")
