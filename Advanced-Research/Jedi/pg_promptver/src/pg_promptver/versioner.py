from __future__ import annotations

from datetime import datetime
from typing import Any

from pg_promptver.models import PromptTemplate, PromptVersion


class PromptVersioner:
    def __init__(self) -> None:
        self._versions: list[PromptVersion] = []
        self._current_idx: int = -1

    def commit(
        self, template: PromptTemplate, message: str = "", tags: tuple[str, ...] = ()
    ) -> PromptVersion:
        version_num = len(self._versions) + 1
        version = PromptVersion(
            version_id=f"v{version_num}",
            template=template,
            created_at=datetime.utcnow(),
            message=message,
            tags=tags,
        )
        self._versions.append(version)
        self._current_idx = len(self._versions) - 1
        return version

    @property
    def current(self) -> PromptVersion | None:
        if self._current_idx < 0:
            return None
        return self._versions[self._current_idx]

    def rollback(self, version_id: str) -> PromptVersion:
        for i, v in enumerate(self._versions):
            if v.version_id == version_id:
                self._current_idx = i
                return v
        raise KeyError(f"Version {version_id} not found")

    def list_versions(self) -> list[PromptVersion]:
        return list(self._versions)

    def get_by_tag(self, tag: str) -> list[PromptVersion]:
        return [v for v in self._versions if tag in v.tags]

    def diff(self, v1_id: str, v2_id: str) -> dict[str, Any]:
        v1 = next((v for v in self._versions if v.version_id == v1_id), None)
        v2 = next((v for v in self._versions if v.version_id == v2_id), None)
        if not v1 or not v2:
            raise KeyError("Version not found")
        changes: dict[str, Any] = {}
        if v1.template.system_prompt != v2.template.system_prompt:
            changes["system_prompt"] = (v1.template.system_prompt, v2.template.system_prompt)
        if v1.template.user_template != v2.template.user_template:
            changes["user_template"] = (v1.template.user_template, v2.template.user_template)
        if v1.template.model != v2.template.model:
            changes["model"] = (v1.template.model, v2.template.model)
        return changes
