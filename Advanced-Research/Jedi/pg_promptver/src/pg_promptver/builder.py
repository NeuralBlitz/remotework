from __future__ import annotations

from pg_promptver.models import PromptTemplate


class PromptBuilder:
    def __init__(self) -> None:
        self._name: str = ""
        self._system: str = ""
        self._user_template: str = ""
        self._variables: list[str] = []
        self._model: str = "gpt-4"
        self._temperature: float = 0.7
        self._max_tokens: int = 1024

    def with_name(self, name: str) -> PromptBuilder:
        self._name = name
        return self

    def with_system(self, system: str) -> PromptBuilder:
        self._system = system
        return self

    def with_user_template(self, template: str) -> PromptBuilder:
        self._user_template = template
        self._variables = self._extract_variables(template)
        return self

    def with_model(self, model: str) -> PromptBuilder:
        self._model = model
        return self

    def with_temperature(self, temp: float) -> PromptBuilder:
        self._temperature = temp
        return self

    def with_max_tokens(self, tokens: int) -> PromptBuilder:
        self._max_tokens = tokens
        return self

    def build(self) -> PromptTemplate:
        if not self._name:
            raise ValueError("Prompt name is required")
        if not self._user_template:
            raise ValueError("User template is required")
        return PromptTemplate(
            name=self._name,
            system_prompt=self._system,
            user_template=self._user_template,
            variables=self._variables,
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
        )

    @staticmethod
    def _extract_variables(template: str) -> list[str]:
        import re

        return list(set(re.findall(r"\{(\w+)\}", template)))
