"""
Granular Arithmetic System
==========================

Implements the mathematical foundations of granular computation over heterogeneous data.

Mathematical Foundations:
- Granule Space: (X, μ, τ) where X ⊆ ℝⁿ, μ: X → [0,1], τ: X → T
- Operations: ⊕ (addition), ⊗ (fusion), ↓ (projection)
- Uncertainty Propagation: Lipschitz-bounded transformations

References:
- Zadeh, L. (1997). "Toward a theory of fuzzy information granulation"
- Pedrycz, W. (2013). "Granular Computing: Analysis and Design"
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, Callable, Optional, List, Dict, Any
from enum import Enum
import numpy as np
import torch
from abc import ABC, abstractmethod


class GranuleType(Enum):
    """Enumeration of supported granule data types."""
    VECTOR = "vector"
    SCALAR = "scalar"
    CATEGORICAL = "categorical"
    ORDINAL = "ordinal"
    INTERVAL = "interval"
    GRAPH = "graph"
    MIXED = "mixed"


@dataclass
class Granule:
    """
    A granule encapsulates data with type information and epistemic uncertainty.
    
    Attributes:
        value: The actual data (numpy array, scalar, or structured object)
        confidence: Epistemic uncertainty ∈ [0, 1], where 1 = certain
        dtype: Type tag from GranuleType
        metadata: Optional additional information (source, lineage, etc.)
    
    Mathematical Definition:
        g = (x, μ, τ) where:
        - x ∈ X (value space)
        - μ ∈ [0,1] (confidence measure)
        - τ ∈ T (type system)
    """
    value: Union[np.ndarray, torch.Tensor, float, int, str, List, Dict]
    confidence: float = 1.0
    dtype: GranuleType = GranuleType.VECTOR
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate granule invariants."""
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be in [0,1], got {self.confidence}")
        
        # Convert to appropriate internal representation
        if isinstance(self.value, (int, float)) and self.dtype == GranuleType.VECTOR:
            self.value = np.array([self.value])
        elif isinstance(self.value, list) and self.dtype == GranuleType.VECTOR:
            self.value = np.array(self.value)
    
    def __add__(self, other: Granule) -> Granule:
        """
        Granular addition: g₁ ⊕ g₂
        
        Type Rules:
            VECTOR ⊕ VECTOR → VECTOR (element-wise addition)
            SCALAR ⊕ SCALAR → SCALAR (scalar addition)
            _ ⊕ _ → TypeError (incompatible types)
        
        Uncertainty Update:
            μ_out = min(μ₁, μ₂)  # Pessimistic aggregation
        """
        if self.dtype != other.dtype:
            raise TypeError(f"Cannot add {self.dtype} and {other.dtype}")
        
        if self.dtype in [GranuleType.VECTOR, GranuleType.SCALAR]:
            result_value = self.value + other.value
            result_confidence = min(self.confidence, other.confidence)
            
            return Granule(
                value=result_value,
                confidence=result_confidence,
                dtype=self.dtype,
                metadata={"operation": "add", "operands": [self.metadata, other.metadata]}
            )
        else:
            raise NotImplementedError(f"Addition not defined for {self.dtype}")
    
    def __mul__(self, other: Union[Granule, float]) -> Granule:
        """Scalar multiplication or element-wise product."""
        if isinstance(other, (int, float)):
            return Granule(
                value=self.value * other,
                confidence=self.confidence,
                dtype=self.dtype,
                metadata=self.metadata
            )
        elif isinstance(other, Granule):
            return self.fuse(other)
        else:
            raise TypeError(f"Cannot multiply Granule with {type(other)}")
    
    def fuse(self, other: Granule) -> Granule:
        """
        Granular fusion: g₁ ⊗ g₂
        
        Context-aware combination that preserves heterogeneity.
        
        Mathematical Definition:
            g₁ ⊗ g₂ = (x₁:₂, μ₁ · μ₂, concat(τ₁, τ₂))
        
        where x₁:₂ is concatenation or aligned join.
        """
        # Type-specific fusion strategies
        if self.dtype == GranuleType.VECTOR and other.dtype == GranuleType.VECTOR:
            # Concatenate vectors
            fused_value = np.concatenate([
                np.atleast_1d(self.value), 
                np.atleast_1d(other.value)
            ])
            fused_dtype = GranuleType.VECTOR
        elif self.dtype == GranuleType.CATEGORICAL and other.dtype == GranuleType.CATEGORICAL:
            # Multi-set union
            fused_value = {**self.value, **other.value}
            fused_dtype = GranuleType.CATEGORICAL
        else:
            # Heterogeneous fusion → MIXED type
            fused_value = {"g1": self.value, "g2": other.value}
            fused_dtype = GranuleType.MIXED
        
        # Confidence: product rule (independent combination)
        fused_confidence = self.confidence * other.confidence
        
        return Granule(
            value=fused_value,
            confidence=fused_confidence,
            dtype=fused_dtype,
            metadata={
                "operation": "fuse",
                "sources": [self.metadata, other.metadata]
            }
        )
    
    def project(self, 
                projection: Callable[[np.ndarray], np.ndarray],
                lipschitz_constant: Optional[float] = None) -> Granule:
        """
        Granular projection: g ↓_P
        
        Applies transformation while tracking uncertainty propagation.
        
        Mathematical Definition:
            g ↓_P = (P(x), μ · exp(-L_P · r), τ')
        
        where:
            - L_P: Lipschitz constant of P
            - r: uncertainty radius
            
        Theorem (Uncertainty Propagation):
            For L-Lipschitz P, perturbations of size r amplify to L·r,
            hence confidence decreases exponentially with L·r.
        """
        if not callable(projection):
            raise TypeError("Projection must be callable")
        
        # Apply transformation
        projected_value = projection(self.value)
        
        # Estimate Lipschitz constant if not provided
        if lipschitz_constant is None:
            lipschitz_constant = self._estimate_lipschitz(projection)
        
        # Uncertainty radius (inverse of confidence)
        uncertainty_radius = 1.0 - self.confidence
        
        # Confidence update: decreases with Lipschitz constant
        # exp(-L·r) ≈ 1 - L·r for small L·r (first-order Taylor)
        projected_confidence = self.confidence * np.exp(-lipschitz_constant * uncertainty_radius)
        projected_confidence = max(0.0, min(1.0, projected_confidence))  # Clip to [0,1]
        
        return Granule(
            value=projected_value,
            confidence=projected_confidence,
            dtype=self._infer_projected_type(projected_value),
            metadata={
                "operation": "project",
                "lipschitz": lipschitz_constant,
                "source": self.metadata
            }
        )
    
    def _estimate_lipschitz(self, func: Callable, num_samples: int = 100) -> float:
        """
        Estimate Lipschitz constant via finite differences.
        
        L_f ≈ max_{x,y} ||f(x) - f(y)|| / ||x - y||
        """
        if not isinstance(self.value, np.ndarray):
            return 1.0  # Conservative default
        
        x = self.value
        samples = [x + np.random.randn(*x.shape) * 0.01 for _ in range(num_samples)]
        
        lipschitz_estimates = []
        for y in samples:
            try:
                fx = func(x)
                fy = func(y)
                numerator = np.linalg.norm(fx - fy)
                denominator = np.linalg.norm(x - y)
                if denominator > 1e-10:
                    lipschitz_estimates.append(numerator / denominator)
            except:
                pass
        
        return max(lipschitz_estimates) if lipschitz_estimates else 1.0
    
    def _infer_projected_type(self, value: Any) -> GranuleType:
        """Infer type of projected value."""
        if isinstance(value, np.ndarray):
            return GranuleType.VECTOR if value.ndim > 0 else GranuleType.SCALAR
        elif isinstance(value, (int, float)):
            return GranuleType.SCALAR
        elif isinstance(value, dict):
            return GranuleType.CATEGORICAL
        else:
            return GranuleType.MIXED
    
    def to_tensor(self) -> torch.Tensor:
        """Convert granule value to PyTorch tensor."""
        if isinstance(self.value, torch.Tensor):
            return self.value
        elif isinstance(self.value, np.ndarray):
            return torch.from_numpy(self.value).float()
        elif isinstance(self.value, (int, float)):
            return torch.tensor([self.value], dtype=torch.float32)
        else:
            raise TypeError(f"Cannot convert {type(self.value)} to tensor")
    
    def __repr__(self) -> str:
        value_str = str(self.value)
        if len(value_str) > 50:
            value_str = value_str[:47] + "..."
        return f"Granule(value={value_str}, μ={self.confidence:.3f}, τ={self.dtype.value})"


class GranuleSpace:
    """
    A collection of granules forming a structured space.
    
    Mathematical Definition:
        𝒢 = {g₁, g₂, ..., gₙ} with operations ⊕, ⊗, ↓
    
    Supports:
        - Batch operations on granules
        - Statistical aggregation with uncertainty
        - Conversion to/from standard ML formats
    """
    
    def __init__(self, granules: List[Granule]):
        self.granules = granules
    
    def __len__(self) -> int:
        return len(self.granules)
    
    def __getitem__(self, idx: int) -> Granule:
        return self.granules[idx]
    
    def map(self, func: Callable[[Granule], Granule]) -> GranuleSpace:
        """Apply function to each granule."""
        return GranuleSpace([func(g) for g in self.granules])
    
    def aggregate(self, method: str = "mean") -> Granule:
        """
        Aggregate granules with uncertainty-aware statistics.
        
        Methods:
            - mean: Weighted average by confidence
            - max: Maximum value with highest confidence
            - vote: Majority vote (for categorical)
        """
        if method == "mean":
            # Confidence-weighted mean
            values = np.array([g.value for g in self.granules])
            confidences = np.array([g.confidence for g in self.granules])
            
            # Normalize confidences to sum to 1
            weights = confidences / (confidences.sum() + 1e-10)
            
            aggregated_value = np.average(values, weights=weights, axis=0)
            aggregated_confidence = np.mean(confidences)  # Average confidence
            
            return Granule(
                value=aggregated_value,
                confidence=aggregated_confidence,
                dtype=self.granules[0].dtype,
                metadata={"operation": "aggregate", "method": method}
            )
        else:
            raise NotImplementedError(f"Aggregation method '{method}' not implemented")
    
    def to_tensor_batch(self) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Convert to (values, confidences) tensor batch.
        
        Returns:
            values: (batch_size, ...) tensor of values
            confidences: (batch_size,) tensor of confidence scores
        """
        values = torch.stack([g.to_tensor() for g in self.granules])
        confidences = torch.tensor([g.confidence for g in self.granules])
        return values, confidences


# ============================================================================
# Factory Functions
# ============================================================================

def make_granule(value: Any, 
                 confidence: float = 1.0,
                 dtype: Optional[GranuleType] = None) -> Granule:
    """
    Convenience factory for creating granules with type inference.
    
    Examples:
        >>> g = make_granule([1, 2, 3])  # Auto-detects VECTOR
        >>> g = make_granule({"class": "cat"}, dtype=GranuleType.CATEGORICAL)
    """
    if dtype is None:
        # Infer type
        if isinstance(value, (list, np.ndarray)):
            dtype = GranuleType.VECTOR
        elif isinstance(value, (int, float)):
            dtype = GranuleType.SCALAR
        elif isinstance(value, dict):
            dtype = GranuleType.CATEGORICAL
        else:
            dtype = GranuleType.MIXED
    
    return Granule(value=value, confidence=confidence, dtype=dtype)


def from_numpy(array: np.ndarray, confidences: Optional[np.ndarray] = None) -> GranuleSpace:
    """Create GranuleSpace from numpy arrays."""
    if confidences is None:
        confidences = np.ones(len(array))
    
    granules = [
        Granule(value=val, confidence=conf, dtype=GranuleType.VECTOR)
        for val, conf in zip(array, confidences)
    ]
    return GranuleSpace(granules)


if __name__ == "__main__":
    # Demo and tests
    print("=== Granular Arithmetic Demo ===\n")
    
    # Create granules
    g1 = make_granule([1.0, 2.0, 3.0], confidence=0.9)
    g2 = make_granule([0.5, 0.5, 0.5], confidence=0.8)
    
    print(f"g1: {g1}")
    print(f"g2: {g2}\n")
    
    # Addition
    g3 = g1 + g2
    print(f"g1 ⊕ g2: {g3}\n")
    
    # Fusion
    g4 = g1.fuse(g2)
    print(f"g1 ⊗ g2: {g4}\n")
    
    # Projection
    def normalize(x):
        return x / (np.linalg.norm(x) + 1e-10)
    
    g5 = g1.project(normalize, lipschitz_constant=2.0)
    print(f"g1 ↓_normalize: {g5}\n")
    
    # Batch operations
    space = GranuleSpace([g1, g2, g3])
    agg = space.aggregate(method="mean")
    print(f"Aggregated: {agg}\n")
    
    print("✓ All operations completed successfully")
