"""
GraNT: Granular Numerical Tensor Framework
===========================================

A mathematically rigorous framework for next-generation ML/AI architectures.

Components:
- core.granule: Granular arithmetic with uncertainty propagation
- core.sheaf_attention: Sheaf-theoretic attention mechanisms
- workflows.sepa: Self-evolving prompt architecture
- workflows.auto_cognition: Autonomous AI research engine
"""

__version__ = "0.1.0"
__author__ = "NeuralBlitz"
__email__ = "NuralNexus@icloud.com"

# Core exports
from grant.core.granule import (
    Granule,
    GranuleSpace,
    GranuleType,
    make_granule,
    from_numpy,
)

from grant.core.sheaf_attention import (
    Poset,
    CocycleAttention,
    SheafAttentionLayer,
    SheafTransformer,
    create_hierarchical_poset,
)

from grant.workflows.sepa import (
    Outcome,
    PromptTemplate,
    OutcomeTracker,
    SEPAEngine,
)

from grant.workflows.auto_cognition import (
    ResearchGoal,
    Solution,
    AutoCognitionEngine,
)

__all__ = [
    # Granular arithmetic
    "Granule",
    "GranuleSpace",
    "GranuleType",
    "make_granule",
    "from_numpy",
    
    # Sheaf attention
    "Poset",
    "CocycleAttention",
    "SheafAttentionLayer",
    "SheafTransformer",
    "create_hierarchical_poset",
    
    # SEPA
    "Outcome",
    "PromptTemplate",
    "OutcomeTracker",
    "SEPAEngine",
    
    # AutoCognition
    "ResearchGoal",
    "Solution",
    "AutoCognitionEngine",
]
