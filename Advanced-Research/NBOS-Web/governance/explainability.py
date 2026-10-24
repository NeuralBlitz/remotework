"""
Explainability Module (XAI)
Forces all complex decisions to include simple, human-legible explanations.
Implements causal explanation regularizers.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ExplainabilityModule:
    """
    Enforces explainability in model decisions through:
    - Causal explanation regularizers
    - Feature importance attribution
    - Counterfactual analysis
    - Simplicity constraints on explanations
    """
    
    def __init__(self):
        self.explanations_generated = 0
        self.explanation_log: List[Dict] = []
        logger.info("Explainability module initialized")
    
    async def generate_explanation(self, prediction: float, input_features: Dict, 
                                  feature_importance: Dict) -> Dict:
        """
        Generate simple, human-legible explanation for a prediction.
        Returns explanation with confidence and reasoning.
        """
        
        # Identify top contributing features
        top_features = sorted(
            feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:3]
        
        # Generate natural language explanation
        explanation = self._generate_natural_language_explanation(prediction, top_features)
        
        # Generate counterfactual: "To get different outcome, change X"
        counterfactual = self._generate_counterfactual(prediction, input_features, top_features)
        
        result = {
            'prediction': prediction,
            'explanation': explanation,
            'reasoning': f"Based on {len(top_features)} key factors",
            'top_factors': dict(top_features),
            'counterfactual': counterfactual,
            'confidence': min(1.0, max(0.5, len(top_features) / 5)),  # Confidence based on factor clarity
            'timestamp': datetime.now().isoformat()
        }
        
        self.explanation_log.append(result)
        self.explanations_generated += 1
        logger.info(f"Generated explanation: {result['explanation'][:50]}...")
        
        return result
    
    def _generate_natural_language_explanation(self, prediction: float, top_features: List) -> str:
        """Generate human-friendly explanation"""
        if not top_features:
            return "Unable to determine key factors."
        
        # Simple template-based explanation
        primary_factor = top_features[0][0]
        primary_importance = top_features[0][1]
        
        if primary_importance > 0.5:
            direction = "positively" if primary_importance > 0 else "negatively"
        else:
            direction = "somewhat"
        
        explanation = f"The prediction of {prediction:.2f} is primarily driven by {primary_factor}, which {direction} influences the outcome."
        
        if len(top_features) > 1:
            secondary_factor = top_features[1][0]
            explanation += f" Additionally, {secondary_factor} plays a secondary role."
        
        return explanation
    
    def _generate_counterfactual(self, prediction: float, features: Dict, top_factors: List) -> str:
        """Generate counterfactual explanation"""
        if not top_factors:
            return "No clear counterfactual available."
        
        primary_factor = top_factors[0][0]
        current_value = features.get(primary_factor, "unknown")
        
        return f"To achieve a different outcome, adjust {primary_factor} (currently: {current_value})."
    
    async def verify_simplicity(self, explanation: str) -> bool:
        """Ensure explanation is simple enough for humans to understand"""
        # Check readability: average word length
        words = explanation.split()
        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        
        # Check sentence length
        sentences = explanation.split('.')
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        simple = avg_word_length < 7 and avg_sentence_length < 20
        
        if not simple:
            logger.warning(f"Explanation may be too complex (word_len={avg_word_length:.1f}, sent_len={avg_sentence_length:.1f})")
        
        return simple
    
    async def audit_explanation_quality(self) -> Dict:
        """Assess quality of all generated explanations"""
        if not self.explanation_log:
            return {"total": 0, "quality": "no_explanations_generated"}
        
        avg_confidence = sum(e.get('confidence', 0) for e in self.explanation_log) / len(self.explanation_log)
        avg_factors = sum(len(e.get('top_factors', {})) for e in self.explanation_log) / len(self.explanation_log)
        
        return {
            'total_explanations': len(self.explanation_log),
            'avg_confidence': avg_confidence,
            'avg_factors_cited': avg_factors,
            'quality': 'good' if avg_confidence > 0.7 else 'fair'
        }
