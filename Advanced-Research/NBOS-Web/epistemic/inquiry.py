"""
Active Epistemic Inquiry Module
Continuous self-assessment to identify knowledge gaps that could lead to biased outcomes.
"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)


class EpistemicInquiry:
    """
    Active epistemic inquiry into knowledge gaps and uncertainty.
    Identifies areas where the model lacks information and could produce biased outputs.
    """
    
    def __init__(self):
        self.knowledge_gaps: List[Dict] = []
        self.uncertainty_regions: List[Dict] = []
        self.inquiry_log: List[Dict] = []
        logger.info("Epistemic Inquiry module initialized")
    
    async def identify_knowledge_gaps(self, input_domain: str, input_features: Dict) -> List[Dict]:
        """
        Systematically identify areas where model knowledge is incomplete.
        Returns list of detected gaps and recommendations.
        """
        gaps = []
        
        # Check feature coverage
        essential_features = self._get_essential_features_for_domain(input_domain)
        provided_features = set(input_features.keys())
        missing = essential_features - provided_features
        
        if missing:
            gap = {
                'type': 'missing_features',
                'domain': input_domain,
                'missing_features': list(missing),
                'severity': 'high' if len(missing) > 2 else 'medium',
                'timestamp': datetime.now().isoformat(),
                'recommendation': f"Collect data on {', '.join(missing)}"
            }
            gaps.append(gap)
            self.knowledge_gaps.append(gap)
        
        # Check for underrepresented subgroups
        underrep_groups = await self._check_demographic_coverage(input_features)
        if underrep_groups:
            gaps.extend(underrep_groups)
        
        # Check model confidence on this input type
        confidence_gap = await self._assess_confidence_gap(input_domain, input_features)
        if confidence_gap:
            gaps.append(confidence_gap)
        
        self._audit_inquiry(f"Identified {len(gaps)} knowledge gaps", {'gaps': len(gaps)})
        return gaps
    
    def _get_essential_features_for_domain(self, domain: str) -> set:
        """Define essential features for different domains"""
        domain_features = {
            'medical': {'patient_age', 'symptoms', 'medical_history', 'vitals'},
            'credit': {'income', 'credit_history', 'debt', 'employment_history'},
            'hiring': {'qualifications', 'experience', 'performance_history'},
            'content': {'user_history', 'semantic_content', 'context'},
        }
        return domain_features.get(domain, set())
    
    async def _check_demographic_coverage(self, input_features: Dict) -> List[Dict]:
        """Check if underrepresented demographic groups are handled"""
        gaps = []
        demographic_attrs = ['age', 'race', 'gender', 'disability_status']
        
        # Check for demographic information
        demographics_present = any(attr in str(input_features).lower() for attr in demographic_attrs)
        
        if not demographics_present:
            # This is okay - we may not have demographic info
            # But we should track that model behavior on unspecified demographics is unverified
            gap = {
                'type': 'demographic_unknown',
                'severity': 'medium',
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Verify model behavior across demographic groups in testing'
            }
            gaps.append(gap)
        
        return gaps
    
    async def _assess_confidence_gap(self, domain: str, features: Dict) -> Dict:
        """Assess areas where model confidence is low"""
        # Simplified: if features are sparse, confidence should be lower
        feature_count = len(features)
        
        if feature_count < 3:
            return {
                'type': 'low_feature_density',
                'severity': 'high',
                'timestamp': datetime.now().isoformat(),
                'recommendation': f'Only {feature_count} features provided; recommend at least 5',
                'suggested_confidence_cap': 0.6
            }
        
        return None
    
    async def detect_distribution_shift(self, new_input: Dict, baseline_stats: Dict) -> Dict:
        """
        Detect when inputs deviate significantly from training distribution.
        This could indicate the model is operating outside its domain of expertise.
        """
        shift_detected = False
        shift_magnitude = 0.0
        
        # Compare input statistics to baseline
        for feature, value in new_input.items():
            if feature in baseline_stats:
                baseline_mean = baseline_stats[feature].get('mean', 0)
                baseline_std = baseline_stats[feature].get('std', 1)
                
                # Z-score normalization
                z_score = abs((value - baseline_mean) / baseline_std) if baseline_std > 0 else 0
                
                if z_score > 3:  # Beyond 3 standard deviations
                    shift_detected = True
                    shift_magnitude = max(shift_magnitude, z_score)
        
        return {
            'shift_detected': shift_detected,
            'shift_magnitude': shift_magnitude,
            'recommendation': 'Apply additional caution; consider human review' if shift_detected else None,
            'suggested_confidence_cap': max(0.5, 1.0 - (shift_magnitude / 10)) if shift_detected else 1.0
        }
    
    def _audit_inquiry(self, event: str, details: Dict) -> None:
        """Log epistemic inquiry activity"""
        self.inquiry_log.append({
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'details': details
        })
    
    def get_uncertainty_summary(self) -> Dict:
        """Summarize all identified uncertainties and knowledge gaps"""
        return {
            'total_gaps_identified': len(self.knowledge_gaps),
            'high_severity': len([g for g in self.knowledge_gaps if g.get('severity') == 'high']),
            'recent_gaps': self.knowledge_gaps[-3:] if self.knowledge_gaps else [],
            'inquiry_events': len(self.inquiry_log),
            'status': 'gaps_present' if self.knowledge_gaps else 'no_known_gaps'
        }
