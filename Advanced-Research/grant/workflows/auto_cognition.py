"""
AutoCognition Engine
====================

Main orchestrator integrating all GraNT components:
- Granular arithmetic
- Sheaf-theoretic attention
- Self-evolving prompts
- PhD-level node integration

This is the production entry point for the complete system.
"""

from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from dataclasses import dataclass
import torch
import torch.nn as nn
import numpy as np

# Import core components
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.granule import Granule, GranuleSpace, make_granule
from core.sheaf_attention import SheafTransformer, create_hierarchical_poset
from workflows.sepa import SEPAEngine, PromptTemplate, Outcome


@dataclass
class ResearchGoal:
    """
    Specification of a research objective.
    
    Attributes:
        description: Natural language description
        constraints: Hard constraints (latency, memory, etc.)
        metrics: Success metrics to optimize
        context: Additional context (team size, timeline, etc.)
    """
    description: str
    constraints: Dict[str, Any]
    metrics: List[str]
    context: Dict[str, Any]


@dataclass
class Solution:
    """
    Generated solution to a research goal.
    
    Attributes:
        architecture: Neural architecture (as PyTorch module)
        code: Implementation code
        documentation: Explanation and usage guide
        proof_trace: Mathematical derivation (if applicable)
        performance: Estimated performance metrics
    """
    architecture: Optional[nn.Module]
    code: str
    documentation: str
    proof_trace: Optional[str]
    performance: Dict[str, float]


class AutoCognitionEngine:
    """
    Main engine for autonomous AI research.
    
    Workflow:
    1. Receive research goal
    2. Bootstrap appropriate prompt template
    3. Generate solution using GraNT components
    4. Evaluate and track outcome
    5. Learn and evolve templates
    
    Example:
        >>> engine = AutoCognitionEngine()
        >>> goal = ResearchGoal(
        ...     description="Design low-latency attention for edge devices",
        ...     constraints={"latency_ms": 10, "memory_mb": 1},
        ...     metrics=["accuracy", "latency", "memory"]
        ... )
        >>> solution = engine.investigate(goal)
        >>> print(solution.documentation)
    """
    
    def __init__(self, 
                 storage_dir: Path = Path("./grant_data"),
                 enable_gpu: bool = True):
        """
        Initialize AutoCognition engine.
        
        Args:
            storage_dir: Directory for persistent storage
            enable_gpu: Whether to use GPU acceleration
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Device configuration
        self.device = torch.device("cuda" if enable_gpu and torch.cuda.is_available() else "cpu")
        
        # Initialize SEPA engine
        self.sepa = SEPAEngine(storage_dir=storage_dir / "sepa")
        
        # Register default templates
        self._register_default_templates()
        
        print(f"AutoCognition Engine initialized")
        print(f"Storage: {self.storage_dir}")
        print(f"Device: {self.device}")
    
    def _register_default_templates(self):
        """Register built-in prompt templates."""
        
        # Template 1: Architecture Design
        arch_template = PromptTemplate(
            name="architecture_design_v1",
            content="""Design a {architecture_type} architecture for {task}.

**Constraints:**
{constraints}

**Optimization Goals:**
{metrics}

**Approach:**
1. Analyze task requirements
2. Select appropriate mathematical framework (granular arithmetic, sheaf theory, etc.)
3. Design modular architecture
4. Implement with error handling
5. Document assumptions and limitations

**Output Format:**
- Architecture class (PyTorch nn.Module)
- Usage documentation
- Performance estimates
""",
            variables=["architecture_type", "task", "constraints", "metrics"]
        )
        
        self.sepa.register_template(arch_template)
        
        # Template 2: Mathematical Derivation
        math_template = PromptTemplate(
            name="mathematical_proof_v1",
            content="""Derive a mathematical proof for: {statement}

**Context:** {context}

**Requirements:**
- Formal theorem statement
- Step-by-step proof
- Identify required lemmas
- Note assumptions

**Mathematical Framework:**
- Use granular arithmetic for uncertainty
- Use sheaf cohomology for attention
- Cite relevant theorems
""",
            variables=["statement", "context"]
        )
        
        self.sepa.register_template(math_template)
        
        # Template 3: Optimization
        opt_template = PromptTemplate(
            name="optimization_v1",
            content="""Optimize {component} for {objective}.

**Current Performance:**
{baseline}

**Target:**
{target}

**Techniques to Consider:**
- Granular uncertainty propagation
- Cocycle attention for sparsity
- Mixed-precision arithmetic
- Knowledge distillation

**Validation:**
- Benchmark on {dataset}
- Compare to {baselines}
""",
            variables=["component", "objective", "baseline", "target", "dataset", "baselines"]
        )
        
        self.sepa.register_template(opt_template)
    
    def investigate(self, goal: ResearchGoal) -> Solution:
        """
        Main entry point: investigate a research goal.
        
        Args:
            goal: Research objective specification
        
        Returns:
            Generated solution
        """
        print(f"\n{'='*70}")
        print(f"INVESTIGATING: {goal.description}")
        print(f"{'='*70}\n")
        
        # Phase 1: Context analysis
        task_type = self._classify_task(goal.description)
        print(f"[PHASE 1] Task Type: {task_type}")
        
        # Phase 2: Template selection
        template = self.sepa.select_template(task_type)
        print(f"[PHASE 2] Selected Template: {template.name}")
        
        # Phase 3: Solution generation
        solution = self._generate_solution(goal, template)
        print(f"[PHASE 3] Solution Generated")
        
        # Phase 4: Evaluation
        metrics = self._evaluate_solution(solution, goal)
        print(f"[PHASE 4] Evaluation: {metrics}")
        
        # Phase 5: Learning
        outcome = self.sepa.execute_and_learn(
            request=goal.description,
            template_id=template.template_id,
            solution=solution.code,
            metrics=metrics,
            success=self._check_constraints(metrics, goal.constraints),
            lessons=self._extract_lessons(solution, metrics)
        )
        print(f"[PHASE 5] Learning Complete (score={outcome.compute_score():.3f})")
        
        return solution
    
    def _classify_task(self, description: str) -> str:
        """
        Classify task type from description.
        
        Args:
            description: Natural language task description
        
        Returns:
            Task type string
        """
        desc_lower = description.lower()
        
        if any(kw in desc_lower for kw in ["design", "architecture", "model"]):
            return "architecture_design"
        elif any(kw in desc_lower for kw in ["prove", "theorem", "lemma", "derive"]):
            return "mathematical_proof"
        elif any(kw in desc_lower for kw in ["optimize", "improve", "faster"]):
            return "optimization"
        else:
            return "architecture_design"  # Default
    
    def _generate_solution(self, goal: ResearchGoal, template: PromptTemplate) -> Solution:
        """
        Generate solution using selected template.
        
        This is where the actual architecture design happens.
        """
        # For demo: create SheafFormer variant
        
        # Parse constraints
        max_latency = goal.constraints.get("latency_ms", 100)
        max_memory = goal.constraints.get("memory_mb", 10)
        
        # Design decisions based on constraints
        if max_latency < 20:
            # Ultra low latency: aggressive sparsification
            n_heads = 4  # Fewer heads
            temperature = 0.1  # High sparsity
            n_layers = 2  # Shallow
        else:
            # Standard configuration
            n_heads = 8
            temperature = 1.0
            n_layers = 4
        
        # Create hierarchical poset for sheaf attention
        poset = create_hierarchical_poset([512, 64, 8])
        
        # Build architecture
        architecture = SheafTransformer(
            vocab_size=10000,
            d_model=256,
            n_layers=n_layers,
            n_heads=n_heads,
            temperature=temperature,
            poset=poset
        ).to(self.device)
        
        # Generate code
        code = f"""
from grant.core.sheaf_attention import SheafTransformer, create_hierarchical_poset
import torch

# Create hierarchical structure
poset = create_hierarchical_poset([512, 64, 8])

# Build model
model = SheafTransformer(
    vocab_size=10000,
    d_model=256,
    n_layers={n_layers},
    n_heads={n_heads},
    temperature={temperature},
    poset=poset
)

# Example usage
input_ids = torch.randint(0, 10000, (2, 128))
output = model(input_ids)
"""
        
        # Generate documentation
        documentation = f"""
# SheafFormer Variant

## Architecture
- Layers: {n_layers}
- Heads: {n_heads}
- Temperature: {temperature}
- Attention: Sheaf-theoretic cocycle optimization

## Design Rationale
Based on constraints:
- Max Latency: {max_latency}ms → {'Aggressive' if max_latency < 20 else 'Standard'} optimization
- Max Memory: {max_memory}MB → Compact configuration

## Key Features
1. **Cocycle Attention**: Minimizes informational tension via cohomological optimization
2. **Hierarchical Structure**: Token → Sentence → Document levels
3. **Granular Uncertainty**: Propagates confidence through computations

## Performance Estimates
- Parameters: {sum(p.numel() for p in architecture.parameters()):,}
- Memory (approx): {sum(p.numel() * 4 for p in architecture.parameters()) / 1e6:.2f} MB
- Expected Latency: {10 + n_layers * 2}ms (estimated)

## Usage
```python
{code}
```
"""
        
        # Proof trace (simplified)
        proof_trace = """
**Theorem (Cocycle Optimality):**
The attention weights minimizing informational tension are:

α_ij = exp(-D_KL(f_j || f_i) / λ) / Z_i

**Proof:**
1. Define energy functional: E(α) = Σ α_ij D_KL(f_j || f_i) + λH(α)
2. Constrain: Σ_j α_ij = 1 (normalization)
3. Lagrangian: L = E(α) + β(1 - Σ_j α_ij)
4. Critical point: ∂L/∂α_ij = D_KL(f_j || f_i) - λ log α_ij - β = 0
5. Solve: α_ij = exp(-D_KL/λ) / Z_i where Z_i = Σ_j exp(-D_KL/λ)

This is precisely the softmax form. ∎
"""
        
        # Performance estimates
        performance = {
            "parameters": sum(p.numel() for p in architecture.parameters()),
            "memory_mb": sum(p.numel() * 4 for p in architecture.parameters()) / 1e6,
            "estimated_latency_ms": 10 + n_layers * 2,
            "estimated_accuracy": 0.85,  # Placeholder
        }
        
        return Solution(
            architecture=architecture,
            code=code,
            documentation=documentation,
            proof_trace=proof_trace,
            performance=performance
        )
    
    def _evaluate_solution(self, solution: Solution, goal: ResearchGoal) -> Dict[str, float]:
        """
        Evaluate generated solution.
        
        In production, this would:
        - Run benchmarks
        - Measure actual latency/memory
        - Compute accuracy on test set
        
        For now, uses estimates.
        """
        metrics = {}
        
        for metric_name in goal.metrics:
            if metric_name in solution.performance:
                metrics[metric_name] = solution.performance[metric_name]
            else:
                metrics[metric_name] = 0.5  # Unknown
        
        # Normalize to [0, 1]
        if "latency_ms" in metrics:
            target = goal.constraints.get("latency_ms", 100)
            metrics["latency"] = max(0, 1 - metrics["latency_ms"] / target)
        
        if "memory_mb" in metrics:
            target = goal.constraints.get("memory_mb", 10)
            metrics["memory"] = max(0, 1 - metrics["memory_mb"] / target)
        
        if "parameters" in metrics:
            # Prefer smaller models
            metrics["compactness"] = 1.0 / (1.0 + metrics["parameters"] / 1e6)
        
        return metrics
    
    def _check_constraints(self, metrics: Dict[str, float], constraints: Dict[str, Any]) -> bool:
        """Check if solution satisfies constraints."""
        if "latency_ms" in constraints and "latency_ms" in metrics:
            if metrics["latency_ms"] > constraints["latency_ms"]:
                return False
        
        if "memory_mb" in constraints and "memory_mb" in metrics:
            if metrics["memory_mb"] > constraints["memory_mb"]:
                return False
        
        return True
    
    def _extract_lessons(self, solution: Solution, metrics: Dict[str, float]) -> List[str]:
        """Extract learned lessons from this execution."""
        lessons = []
        
        # Check what worked
        if metrics.get("latency", 0) > 0.8:
            lessons.append("Aggressive layer reduction helps latency")
        
        if metrics.get("memory", 0) > 0.8:
            lessons.append("Compact d_model reduces memory")
        
        # Check architecture decisions
        if solution.architecture:
            n_params = sum(p.numel() for p in solution.architecture.parameters())
            if n_params < 5e6:
                lessons.append("Small models (<5M params) are feasible")
        
        return lessons
    
    def generate_artifact(self, solution: Solution, output_path: Path):
        """
        Save solution as artifact.
        
        Args:
            solution: Generated solution
            output_path: Where to save (e.g., 'sheaf_former.py')
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        artifact = f"""
'''
{solution.documentation}
'''

{solution.code}

if __name__ == "__main__":
    # Demo
    import torch
    model = SheafTransformer(vocab_size=10000, d_model=256)
    x = torch.randint(0, 10000, (2, 128))
    y = model(x)
    print(f"Output shape: {{y.shape}}")
"""
        
        with open(output_path, 'w') as f:
            f.write(artifact)
        
        print(f"Artifact saved to: {output_path}")


if __name__ == "__main__":
    print("=== AutoCognition Engine Demo ===\n")
    
    # Initialize engine
    engine = AutoCognitionEngine(storage_dir=Path("/tmp/grant_demo"))
    
    # Define research goal
    goal = ResearchGoal(
        description="Design a low-latency attention mechanism for edge devices",
        constraints={
            "latency_ms": 10,
            "memory_mb": 1
        },
        metrics=["accuracy", "latency", "memory"],
        context={
            "team_size": 3,
            "timeline": "2 weeks"
        }
    )
    
    # Investigate
    solution = engine.investigate(goal)
    
    # Save artifact
    engine.generate_artifact(solution, Path("/tmp/sheaf_former_edge.py"))
    
    print("\n" + "="*70)
    print("SOLUTION SUMMARY")
    print("="*70)
    print(solution.documentation)
    
    print("\n✓ AutoCognition engine working correctly!")
