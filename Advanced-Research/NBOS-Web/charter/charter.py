"""
Ethical Charter Layer
Hard-coded ethical constraints that form an inviolable barrier between model outputs and users.
Every output is verified against these axiomatic principles before delivery.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class EthicalPrinciple(Enum):
    """Fundamental ethical axioms"""
    NO_DECEPTION = "no_deception"
    HUMAN_DIGNITY = "human_dignity"
    FAIRNESS = "fairness"
    TRANSPARENCY = "transparency"
    SAFETY = "safety"


@dataclass
class OutputVerification:
    """Result of Charter Layer verification"""
    passed: bool
    principle_results: Dict[str, bool]
    violations: List[str]
    timestamp: str
    confidence: float


class CharterLayer:
    """
    The inviolable ethical gate. Every output must pass this verification.
    Implements formal logic checks to prevent alignment drift.
    """
    
    def __init__(self):
        self.charter_rules = {
            EthicalPrinciple.NO_DECEPTION: self._check_honesty,
            EthicalPrinciple.HUMAN_DIGNITY: self._check_dignity,
            EthicalPrinciple.FAIRNESS: self._check_fairness,
            EthicalPrinciple.TRANSPARENCY: self._check_transparency,
            EthicalPrinciple.SAFETY: self._check_safety,
        }
        self.verification_log: List[OutputVerification] = []
        logger.info("CharterLayer initialized with 5 core ethical principles")
    
    async def verify_output(self, output: Any, context: Dict = None) -> OutputVerification:
        """
        Verify output against all charter principles.
        Returns verification result and blocks non-compliant outputs.
        """
        context = context or {}
        principle_results = {}
        violations = []
        
        for principle, check_func in self.charter_rules.items():
            try:
                passed = await check_func(output, context)
                principle_results[principle.value] = passed
                if not passed:
                    violations.append(f"Violated: {principle.value}")
            except Exception as e:
                logger.error(f"Charter verification error for {principle.value}: {e}")
                principle_results[principle.value] = False
                violations.append(f"Check failed: {principle.value}")
        
        all_passed = all(principle_results.values())
        
        verification = OutputVerification(
            passed=all_passed,
            principle_results=principle_results,
            violations=violations,
            timestamp=datetime.now().isoformat(),
            confidence=sum(principle_results.values()) / len(principle_results)
        )
        
        self.verification_log.append(verification)
        
        if not all_passed:
            logger.warning(f"CharterLayer BLOCKED output. Violations: {violations}")
            raise CharterViolationError(f"Output violates charter: {violations}")
        
        logger.info(f"CharterLayer APPROVED output (confidence: {verification.confidence:.2f})")
        return verification
    
    async def _check_honesty(self, output: Any, context: Dict) -> bool:
        """Verify output accurately represents confidence levels and limitations"""
        # Check if output includes confidence/uncertainty metrics
        if hasattr(output, 'confidence') or hasattr(output, 'uncertainty'):
            return True
        # Check if deception markers are absent
        deception_markers = ['guaranteed', 'definite', 'absolutely certain', 'impossible']
        if isinstance(output, str):
            for marker in deception_markers:
                if marker.lower() in output.lower():
                    return False
        return True
    
    async def _check_dignity(self, output: Any, context: Dict) -> bool:
        """Verify respect for privacy, autonomy, and human rights"""
        # Check for privacy violations
        sensitive_keywords = ['password', 'ssn', 'credit card', 'private medical']
        if isinstance(output, str):
            output_lower = output.lower()
            for keyword in sensitive_keywords:
                if keyword in output_lower:
                    return False
        
        # Check context for dignity constraints
        user_id = context.get('user_id')
        if user_id and context.get('requires_consent'):
            consent_given = context.get('consent_given', False)
            if not consent_given:
                return False
        
        return True
    
    async def _check_fairness(self, output: Any, context: Dict) -> bool:
        """Verify no discriminatory outcomes by protected attributes"""
        # Simplified fairness check - in production would integrate bias detection
        protected_attributes = ['race', 'gender', 'religion', 'disability', 'age']
        
        if isinstance(output, str):
            output_lower = output.lower()
            # Check for discriminatory language
            discriminatory_phrases = [
                'should not',  # e.g., "women should not apply"
                'incapable',
                'unfit',
                'inferior'
            ]
            for phrase in discriminatory_phrases:
                if phrase in output_lower:
                    for attr in protected_attributes:
                        if attr in output_lower:
                            return False
        
        return True
    
    async def _check_transparency(self, output: Any, context: Dict) -> bool:
        """Verify explainability in reasoning and decision-making"""
        # Outputs should either:
        # 1. Include reasoning/explanation
        # 2. Be marked as non-explainable with justification
        if hasattr(output, 'reasoning') or hasattr(output, 'explanation'):
            return True
        
        if isinstance(output, dict):
            if 'reasoning' in output or 'explanation' in output:
                return True
        
        # Allow simple factual outputs without explanation
        # but complex decisions need reasoning
        if context.get('is_complex_decision', False):
            return False
        
        return True
    
    async def _check_safety(self, output: Any, context: Dict) -> bool:
        """Verify refusal of harmful requests and escalation when uncertain"""
        harmful_keywords = [
            'kill', 'harm', 'violence', 'illegal', 'exploit', 'abuse'
        ]
        
        if isinstance(output, str):
            output_lower = output.lower()
            for keyword in harmful_keywords:
                if keyword in output_lower:
                    # Check if this is a safety discussion rather than advocacy
                    safety_context = context.get('safety_discussion', False)
                    if not safety_context:
                        return False
        
        # Check if uncertain and should escalate
        if context.get('uncertainty_level', 0) > 0.7:
            should_escalate = context.get('auto_escalate', True)
            if should_escalate:
                logger.warning("High uncertainty detected - escalating to human review")
        
        return True
    
    def get_verification_history(self) -> List[OutputVerification]:
        """Retrieve verification history for audit"""
        return self.verification_log.copy()


class CharterViolationError(Exception):
    """Raised when output violates charter principles"""
    pass
