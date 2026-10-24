"""
Mito Prompt Templates
Template engine, few-shot examples, prompt chaining, variable injection
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field

logger = logging.getLogger("mito.prompts")


@dataclass
class PromptTemplate:
    name: str
    template: str
    variables: List[str] = field(default_factory=list)
    description: str = ""
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.variables = list(set(re.findall(r"\{\{(\w+)\}\}", self.template)))

    def render(self, **kwargs) -> str:
        result = self.template
        for var in self.variables:
            value = kwargs.get(var, "")
            result = result.replace(f"{{{{{var}}}}}", str(value))
        return result

    def validate(self, **kwargs) -> List[str]:
        missing = [v for v in self.variables if v not in kwargs]
        return missing


@dataclass
class FewShotExample:
    input: str
    output: str
    explanation: str = ""


class FewShotTemplate:
    def __init__(self, name: str, instruction: str, examples: List[FewShotExample] = None,
                 input_label: str = "Input:", output_label: str = "Output:"):
        self.name = name
        self.instruction = instruction
        self.examples = examples or []
        self.input_label = input_label
        self.output_label = output_label

    def render(self, input_text: str, max_examples: int = 3) -> str:
        parts = [self.instruction, ""]
        for ex in self.examples[:max_examples]:
            parts.append(f"{self.input_label} {ex.input}")
            parts.append(f"{self.output_label} {ex.output}")
            if ex.explanation:
                parts.append(f"Explanation: {ex.explanation}")
            parts.append("")
        parts.append(f"{self.input_label} {input_text}")
        parts.append(self.output_label)
        return "\n".join(parts)

    def add_example(self, input_text: str, output: str, explanation: str = ""):
        self.examples.append(FewShotExample(input_text, output, explanation))


class PromptChain:
    def __init__(self, name: str = ""):
        self.name = name
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, template: PromptTemplate, output_key: str = None, **defaults) -> "PromptChain":
        self.steps.append({"template": template, "output_key": output_key or template.name, "defaults": defaults})
        return self

    def render(self, initial_vars: Dict[str, Any]) -> List[Dict]:
        context = {**initial_vars}
        results = []
        for step in self.steps:
            template = step["template"]
            merged = {**step["defaults"], **context}
            rendered = template.render(**merged)
            results.append({"step": template.name, "prompt": rendered, "variables": merged})
            context[step["output_key"]] = f"[result of {template.name}]"
        return results


class PromptLibrary:
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.few_shot: Dict[str, FewShotTemplate] = {}
        self._load_defaults()

    def _load_defaults(self):
        self.add(PromptTemplate("summarize", "Summarize the following text in {{style}}:\n\n{{text}}"))
        self.add(PromptTemplate("extract", "Extract {{entity_type}} from the following text:\n\n{{text}}\n\nReturn as JSON."))
        self.add(PromptTemplate("classify", "Classify the following text into one of: {{categories}}\n\nText: {{text}}\n\nCategory:"))
        self.add(PromptTemplate("rewrite", "Rewrite the following text in a {{tone}} tone:\n\n{{text}}"))
        self.add(PromptTemplate("translate", "Translate the following from {{source_lang}} to {{target_lang}}:\n\n{{text}}"))
        self.add(PromptTemplate("explain", "Explain the following {{concept}} in simple terms for a {{audience}} audience."))
        self.add(PromptTemplate("code_review", "Review the following {{language}} code and suggest improvements:\n\n```{{language}}\n{{code}}\n```"))
        self.add(PromptTemplate("generate_sql", "Generate a SQL query for: {{description}}\n\nDatabase schema:\n{{schema}}"))
        self.add(PromptTemplate("chain_of_thought", "Think step by step to solve: {{problem}}"))
        self.add(PromptTemplate("role_play", "You are {{role}}. {{instruction}}\n\nUser: {{input}}"))

    def add(self, template: PromptTemplate):
        self.templates[template.name] = template

    def get(self, name: str) -> Optional[PromptTemplate]:
        return self.templates.get(name)

    def render(self, name: str, **kwargs) -> str:
        template = self.get(name)
        if not template:
            raise KeyError(f"Template '{name}' not found")
        return template.render(**kwargs)

    def list_templates(self, tags: List[str] = None) -> List[PromptTemplate]:
        if not tags:
            return list(self.templates.values())
        return [t for t in self.templates.values() if set(tags) & set(t.tags)]

    def search(self, query: str) -> List[PromptTemplate]:
        query = query.lower()
        return [t for t in self.templates.values()
                if query in t.name.lower() or query in t.description.lower()]
