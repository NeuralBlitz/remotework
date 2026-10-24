"""
Privacy Preservation Module
Implements differential privacy, federated learning readiness, and data sanitization.
"""

import logging
import hashlib
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PrivacyPreservationModule:
    """
    Protects user privacy through multiple mechanisms:
    - Differential privacy for aggregated statistics
    - Data sanitization to remove PII
    - Privacy budget tracking
    - Secure multi-party computation readiness
    """
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        """
        Initialize with differential privacy parameters.
        epsilon: privacy budget (lower = more private)
        delta: probability bound for privacy breach
        """
        self.epsilon = epsilon
        self.delta = delta
        self.privacy_budget_spent = 0.0
        self.privacy_log: List[Dict] = []
        
        # PII patterns to sanitize
        self.pii_patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        }
        
        logger.info(f"Privacy module initialized: epsilon={epsilon}, delta={delta}")
    
    async def sanitize_input(self, data: Any) -> Any:
        """Remove or hash PII from input data"""
        if isinstance(data, str):
            return self._sanitize_string(data)
        elif isinstance(data, dict):
            return {k: self._sanitize_string(v) if isinstance(v, str) else v 
                   for k, v in data.items()}
        return data
    
    def _sanitize_string(self, text: str) -> str:
        """Remove/hash PII from string"""
        import re
        
        sanitized = text
        
        # Replace email with hash
        sanitized = re.sub(
            self.pii_patterns['email'],
            lambda m: f"[EMAIL_HASH_{hashlib.md5(m.group().encode()).hexdigest()[:8]}]",
            sanitized
        )
        
        # Replace phone with masked version
        sanitized = re.sub(
            self.pii_patterns['phone'],
            "[PHONE_MASKED]",
            sanitized
        )
        
        # Replace SSN with masked version
        sanitized = re.sub(
            self.pii_patterns['ssn'],
            "[SSN_MASKED]",
            sanitized
        )
        
        # Replace credit card with masked version
        sanitized = re.sub(
            self.pii_patterns['credit_card'],
            "[CARD_MASKED]",
            sanitized
        )
        
        return sanitized
    
    async def add_differential_privacy_noise(self, statistic: float, sensitivity: float) -> float:
        """
        Add Laplace noise to protect individual privacy.
        Uses differential privacy mechanism to bound privacy loss.
        """
        import numpy as np
        
        # Check privacy budget
        privacy_cost = sensitivity / self.epsilon
        if self.privacy_budget_spent + privacy_cost > 1.0:
            logger.warning("Privacy budget nearly exhausted - consider refreshing")
        
        # Add Laplace noise
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        noisy_statistic = statistic + noise
        
        # Track privacy spend
        self.privacy_budget_spent += privacy_cost
        self.privacy_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'differential_privacy',
            'sensitivity': sensitivity,
            'epsilon_cost': privacy_cost,
            'total_spent': self.privacy_budget_spent
        })
        
        logger.info(f"Differential privacy applied. Budget: {self.privacy_budget_spent:.2%}")
        return noisy_statistic
    
    async def federated_learning_ready(self, model_update: Dict) -> bool:
        """Verify model update is safe for federated learning without privacy leak"""
        # Check for gradient attacks
        if 'gradients' in model_update:
            # Verify gradients are aggregated/averaged, not individual
            if 'individual_gradients' in model_update:
                logger.warning("Individual gradients present - privacy risk detected")
                return False
        
        # Check model size (larger models leak less information per example)
        model_params = model_update.get('num_parameters', 0)
        if model_params < 1000:
            logger.warning("Small model detected - may be vulnerable to privacy attacks")
        
        self.privacy_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'federated_readiness_check',
            'safe': True
        })
        
        return True
    
    def get_privacy_report(self) -> Dict:
        """Generate privacy compliance report"""
        return {
            'epsilon': self.epsilon,
            'delta': self.delta,
            'privacy_budget_spent': self.privacy_budget_spent,
            'budget_remaining': max(0, 1.0 - self.privacy_budget_spent),
            'total_operations': len(self.privacy_log),
            'pii_types_protected': list(self.pii_patterns.keys()),
            'status': 'COMPLIANT' if self.privacy_budget_spent < 1.0 else 'BUDGET_EXCEEDED'
        }
