from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BehaviorNode:
    node_id: str
    node_type: str = ""
    children: list[str] = field(default_factory=list)


@dataclass
class NPCState:
    npc_id: str
    is_hostile: bool = False
    is_low_health: bool = False
    has_target: bool = False
    last_action: str = ""
    position: tuple[float, float] = (0.0, 0.0)

