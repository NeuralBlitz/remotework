"""
Base neural module and configuration classes.
All NBOS components inherit from BaseNeuralModule.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ModuleConfig:
    """Configuration for any neural module"""
    name: str
    version: str
    enabled: bool = True
    governance_level: str = "standard"  # standard, strict, unrestricted
    audit_enabled: bool = True
    max_latency_ms: int = 5000
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseNeuralModule(ABC):
    """
    Base class for all NBOS components.
    Enforces governance compliance, audit logging, and ethical constraints.
    """
    
    def __init__(self, config: ModuleConfig):
        self.config = config
        self.logger = logging.getLogger(f"nbos.{config.name}")
        self.audit_log: list = []
        self.initialization_time = datetime.now()
        self._verify_governance_compliance()
        
    def _verify_governance_compliance(self) -> bool:
        """Verify module meets governance standards before activation"""
        compliance_checks = {
            "name_valid": bool(self.config.name),
            "version_valid": bool(self.config.version),
            "audit_enabled": self.config.audit_enabled,
            "governance_level_valid": self.config.governance_level in ["standard", "strict", "unrestricted"]
        }
        
        if not all(compliance_checks.values()):
            self.logger.error(f"Governance compliance failed: {compliance_checks}")
            raise ValueError("Module does not meet governance standards")
        
        self._audit(f"Governance compliance verified: {compliance_checks}")
        return True
    
    def _audit(self, event: str, details: Optional[Dict] = None) -> None:
        """Log all significant events for audit trail"""
        if self.config.audit_enabled:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "module": self.config.name,
                "event": event,
                "details": details or {}
            }
            self.audit_log.append(audit_entry)
            self.logger.info(f"[AUDIT] {event}")
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input through module"""
        pass
    
    def get_audit_trail(self) -> list:
        """Retrieve complete audit trail for this module"""
        return self.audit_log.copy()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.config.name}, version={self.config.version})"
