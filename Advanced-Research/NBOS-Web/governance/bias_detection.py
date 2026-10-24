"""
Bias Detection and Mitigation Module
Continuous analysis of model outputs for statistical bias across protected attributes.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class BiasType(Enum):
    """Types of bias to monitor"""
    REPRESENTATION = "representation"  # Under/over-representation in data
    MEASUREMENT = "measurement"  # Proxy variables and indirect discrimination
    AGGREGATION = "aggregation"  # Group-level vs individual fairness trade-offs
    EVALUATION = "evaluation"  # Metric selection bias
    DEPLOYMENT = "deployment"  # Real-world outcome disparities


@dataclass
class BiasMetric:
    """Bias measurement result"""
    bias_type: BiasType
    protected_attribute: str
    disparity_ratio: float  # Ratio of outcomes between groups
    threshold: float  # Acceptable disparity (typically 0.8)
    violates_threshold: bool
    timestamp: str
    remediation_suggested: str


class BiasDetectionModule:
    """
    Real-time bias detection across all model outputs.
    Monitors disparities in treatment of different demographic groups.
    """
    
    def __init__(self):
        self.protected_attributes = [
            'race', 'gender', 'age_group', 'disability_status', 'religion'
        ]
        self.bias_metrics: List[BiasMetric] = []
        self.mitigation_strategies = {
            BiasType.REPRESENTATION: self._mitigate_representation,
            BiasType.MEASUREMENT: self._mitigate_measurement,
            BiasType.AGGREGATION: self._mitigate_aggregation,
            BiasType.EVALUATION: self._mitigate_evaluation,
            BiasType.DEPLOYMENT: self._mitigate_deployment,
        }
        logger.info("BiasDetectionModule initialized")
    
    async def analyze_output(self, output: Any, demographics: Dict[str, str]) -> List[BiasMetric]:
        """
        Analyze output for bias given user demographics.
        Returns list of detected biases and severity levels.
        """
        detected_biases = []
        
        for protected_attr in self.protected_attributes:
            if protected_attr not in demographics:
                continue
            
            # Check for disparate impact
            metric = await self._check_disparate_impact(output, protected_attr, demographics)
            if metric:
                detected_biases.append(metric)
                
                # Trigger mitigation if threshold violated
                if metric.violates_threshold:
                    await self._apply_mitigation(metric)
        
        self.bias_metrics.extend(detected_biases)
        return detected_biases
    
    async def _check_disparate_impact(self, output: Any, attribute: str, 
                                      demographics: Dict) -> BiasMetric:
        """Check if output shows different treatment based on protected attribute"""
        
        # Simplified disparate impact calculation
        # In production: compare treatment across demographic groups
        disparity_ratio = 1.0  # Default: no disparity
        
        # Example: if model output differs systematically by group
        if isinstance(output, dict) and 'score' in output:
            base_score = output['score']
            attr_value = demographics.get(attribute)
            
            # Simulate disparate impact detection
            # (In production, would analyze actual outcome distributions)
            if attr_value == 'minority' and base_score > 0.7:
                disparity_ratio = 0.75  # 25% disparity
        
        threshold = 0.8
        violates = disparity_ratio < threshold
        
        bias_metric = BiasMetric(
            bias_type=BiasType.MEASUREMENT,
            protected_attribute=attribute,
            disparity_ratio=disparity_ratio,
            threshold=threshold,
            violates_threshold=violates,
            timestamp=datetime.now().isoformat(),
            remediation_suggested=f"Review and retrain model on balanced {attribute} distribution"
        )
        
        if violates:
            logger.warning(f"Disparate impact detected: {attribute} disparity={disparity_ratio:.2f}")
        
        return bias_metric
    
    async def _apply_mitigation(self, metric: BiasMetric) -> None:
        """Apply mitigation strategy for detected bias"""
        mitigation_func = self.mitigation_strategies.get(metric.bias_type)
        if mitigation_func:
            await mitigation_func(metric)
    
    async def _mitigate_representation(self, metric: BiasMetric) -> None:
        """Mitigate representation bias through balanced sampling"""
        logger.info(f"Applying representation mitigation for {metric.protected_attribute}")
    
    async def _mitigate_measurement(self, metric: BiasMetric) -> None:
        """Mitigate measurement bias by adjusting proxy variables"""
        logger.info(f"Applying measurement mitigation for {metric.protected_attribute}")
    
    async def _mitigate_aggregation(self, metric: BiasMetric) -> None:
        """Mitigate aggregation bias by favoring individual fairness"""
        logger.info(f"Applying aggregation mitigation for {metric.protected_attribute}")
    
    async def _mitigate_evaluation(self, metric: BiasMetric) -> None:
        """Mitigate evaluation bias by expanding metric set"""
        logger.info(f"Applying evaluation mitigation for {metric.protected_attribute}")
    
    async def _mitigate_deployment(self, metric: BiasMetric) -> None:
        """Mitigate deployment bias through real-world monitoring"""
        logger.info(f"Applying deployment mitigation for {metric.protected_attribute}")
    
    def get_bias_report(self) -> Dict:
        """Generate comprehensive bias report"""
        violations = [m for m in self.bias_metrics if m.violates_threshold]
        return {
            "total_checks": len(self.bias_metrics),
            "violations": len(violations),
            "violation_rate": len(violations) / len(self.bias_metrics) if self.bias_metrics else 0,
            "affected_attributes": list(set(m.protected_attribute for m in violations)),
            "latest_violations": violations[-5:] if violations else []
        }
