from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ShaderAST:
    source: str = ""
    nodes: list[dict[str, str]] = field(default_factory=list)
    uniforms: list[str] = field(default_factory=list)


@dataclass
class CompiledShader:
    shader_id: str
    source: str = ""
    uniform_count: int = 0
    instruction_count: int = 0

