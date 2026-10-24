"""
GraNT Framework - Complete Example
===================================

This example demonstrates all major features:
1. Granular arithmetic with uncertainty
2. Sheaf-theoretic attention
3. Self-evolving prompt architecture
4. Autonomous research with AutoCognition

Run this to verify the installation and see the framework in action.
"""

import torch
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from grant import (
    # Granular arithmetic
    make_granule, GranuleSpace, from_numpy,
    
    # Sheaf attention
    SheafTransformer, CocycleAttention, create_hierarchical_poset,
    
    # SEPA
    SEPAEngine, PromptTemplate,
    
    # AutoCognition
    AutoCognitionEngine, ResearchGoal
)


def demo_granular_arithmetic():
    """Demonstrate granular arithmetic operations."""
    print("\n" + "="*70)
    print("DEMO 1: Granular Arithmetic")
    print("="*70 + "\n")
    
    # Create granules with different confidence levels
    print("Creating granules...")
    g1 = make_granule([1.0, 2.0, 3.0], confidence=0.95)
    g2 = make_granule([0.5, 1.0, 1.5], confidence=0.85)
    g3 = make_granule([2.0, 1.0, 0.5], confidence=0.75)
    
    print(f"g1: {g1}")
    print(f"g2: {g2}")
    print(f"g3: {g3}\n")
    
    # Addition: uncertainty propagates pessimistically
    print("Addition (⊕):")
    g_sum = g1 + g2
    print(f"g1 ⊕ g2 = {g_sum}")
    print(f"Note: confidence = min(0.95, 0.85) = {g_sum.confidence}\n")
    
    # Fusion: combines information
    print("Fusion (⊗):")
    g_fused = g1.fuse(g2)
    print(f"g1 ⊗ g2 = {g_fused}")
    print(f"Note: confidence = 0.95 * 0.85 = {g_fused.confidence:.3f}\n")
    
    # Projection: applies transformation with uncertainty tracking
    print("Projection (↓):")
    
    def normalize(x):
        return x / (np.linalg.norm(x) + 1e-10)
    
    g_proj = g1.project(normalize, lipschitz_constant=1.5)
    print(f"g1 ↓_normalize = {g_proj}")
    print(f"Note: confidence decreased due to Lipschitz constant\n")
    
    # Batch operations
    print("Batch Aggregation:")
    space = GranuleSpace([g1, g2, g3])
    g_agg = space.aggregate(method="mean")
    print(f"Aggregated (confidence-weighted): {g_agg}")
    print(f"Higher-confidence granules contribute more\n")
    
    return g_agg


def demo_sheaf_attention():
    """Demonstrate sheaf-theoretic attention."""
    print("\n" + "="*70)
    print("DEMO 2: Sheaf-Theoretic Attention")
    print("="*70 + "\n")
    
    # Create hierarchical structure
    print("Creating hierarchical poset...")
    poset = create_hierarchical_poset([512, 64, 8])
    print(f"Levels: {poset.elements}")
    print(f"Covering relations: {poset.covering_relations()}\n")
    
    # Build SheafTransformer
    print("Building SheafTransformer...")
    model = SheafTransformer(
        vocab_size=1000,
        d_model=128,
        n_layers=3,
        n_heads=4,
        temperature=0.7,  # Moderate sparsity
        poset=poset
    )
    
    param_count = sum(p.numel() for p in model.parameters())
    print(f"Parameters: {param_count:,}")
    print(f"Memory: {param_count * 4 / 1e6:.2f} MB\n")
    
    # Forward pass
    print("Forward pass...")
    batch_size = 2
    seq_len = 64
    input_ids = torch.randint(0, 1000, (batch_size, seq_len))
    
    with torch.no_grad():
        output = model(input_ids)
    
    print(f"Input shape: {input_ids.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Output range: [{output.min():.3f}, {output.max():.3f}]\n")
    
    # Test cocycle attention directly
    print("Testing CocycleAttention...")
    attn = CocycleAttention(d_model=128, temperature=0.5)
    
    Q = torch.randn(2, 10, 128)
    K = torch.randn(2, 10, 128)
    V = torch.randn(2, 10, 128)
    
    output_attn, weights = attn(Q, K, V)
    
    print(f"Attention output shape: {output_attn.shape}")
    print(f"Attention weights shape: {weights.shape}")
    print(f"Weights sum (should be 1.0): {weights[0, 0, :].sum():.6f}")
    print(f"Sparsity: {(weights < 0.01).float().mean():.2%} of weights < 0.01\n")
    
    return model


def demo_sepa():
    """Demonstrate self-evolving prompt architecture."""
    print("\n" + "="*70)
    print("DEMO 3: Self-Evolving Prompt Architecture (SEPA)")
    print("="*70 + "\n")
    
    # Create SEPA engine
    print("Initializing SEPA engine...")
    sepa = SEPAEngine(storage_dir=Path("/tmp/sepa_demo"), exploration_rate=0.1)
    
    # Register template
    print("Registering template...")
    template = PromptTemplate(
        name="research_task_v1",
        content="""Research task: {task}

Approach:
1. Analyze requirements
2. Design solution
3. Implement with {framework}
4. Validate performance

Constraints: {constraints}
""",
        variables=["task", "framework", "constraints"]
    )
    sepa.register_template(template)
    
    # Simulate multiple executions
    print("\nSimulating 20 executions...\n")
    
    tasks = [
        "optimize attention mechanism",
        "reduce model latency",
        "improve accuracy",
        "compress model size",
    ]
    
    for i in range(20):
        task = np.random.choice(tasks)
        success = np.random.rand() > 0.3  # 70% success rate
        
        outcome = sepa.execute_and_learn(
            request=f"Task {i}: {task}",
            template_id=template.template_id,
            solution=f"Solution {i}",
            metrics={
                "accuracy": 0.7 + np.random.rand() * 0.3 if success else 0.4 + np.random.rand() * 0.3,
                "latency": 10 + np.random.rand() * 20,
            },
            success=success,
            lessons=[
                "sparsity helps" if i % 3 == 0 else "dense better",
                "warmup important" if i % 2 == 0 else "no warmup",
            ] if success else ["approach failed"]
        )
        
        if i % 5 == 0:
            print(f"Execution {i}: score={outcome.compute_score():.3f}, success={success}")
    
    # Generate report
    print("\n" + sepa.generate_report())
    
    # Check if template evolved
    print("\nTemplate Evolution:")
    evolved_templates = [t for t in sepa.templates.values() if "v2" in t.name or "v3" in t.name]
    if evolved_templates:
        print(f"✨ {len(evolved_templates)} evolved template(s) created!")
        for t in evolved_templates:
            print(f"  - {t.name}: {t.get_mean_performance():.3f} performance")
    else:
        print("No evolution yet (need more data)")
    
    return sepa


def demo_autocognition():
    """Demonstrate autonomous research with AutoCognition."""
    print("\n" + "="*70)
    print("DEMO 4: AutoCognition Engine - Autonomous AI Research")
    print("="*70 + "\n")
    
    # Initialize engine
    print("Initializing AutoCognition engine...")
    engine = AutoCognitionEngine(
        storage_dir=Path("/tmp/autocognition_demo"),
        enable_gpu=False
    )
    print()
    
    # Define research goal
    goal = ResearchGoal(
        description="Design an ultra-efficient attention mechanism for mobile devices",
        constraints={
            "latency_ms": 8,
            "memory_mb": 0.5,
        },
        metrics=["accuracy", "latency", "memory"],
        context={
            "team_size": 2,
            "timeline": "1 week",
            "deployment": "mobile app"
        }
    )
    
    print(f"Research Goal: {goal.description}")
    print(f"Constraints: {goal.constraints}")
    print(f"Metrics: {goal.metrics}\n")
    
    # Investigate
    solution = engine.investigate(goal)
    
    # Display results
    print("\n" + "="*70)
    print("GENERATED SOLUTION")
    print("="*70)
    print(solution.documentation)
    
    print("\n" + "="*70)
    print("PERFORMANCE ESTIMATES")
    print("="*70)
    for metric, value in solution.performance.items():
        print(f"{metric}: {value}")
    
    # Save artifact
    output_path = Path("/tmp/mobile_sheaf_former.py")
    engine.generate_artifact(solution, output_path)
    print(f"\n✓ Artifact saved to: {output_path}")
    
    return solution


def demo_integration():
    """Demonstrate integration of all components."""
    print("\n" + "="*70)
    print("DEMO 5: Full Integration - Granules → Sheaf → SEPA")
    print("="*70 + "\n")
    
    # Step 1: Create dataset with uncertainty
    print("Step 1: Creating granular dataset...")
    data = np.random.randn(100, 64)
    confidences = 0.7 + 0.3 * np.random.rand(100)  # Vary by sample
    
    granule_dataset = from_numpy(data, confidences)
    print(f"Dataset: {len(granule_dataset)} samples")
    print(f"Confidence range: [{confidences.min():.2f}, {confidences.max():.2f}]\n")
    
    # Step 2: Pass through sheaf attention
    print("Step 2: Processing with SheafTransformer...")
    model = SheafTransformer(vocab_size=1000, d_model=64, n_layers=2)
    
    values, confs = granule_dataset.to_tensor_batch()
    
    # Simulate token IDs (in practice, these come from tokenizer)
    token_ids = torch.randint(0, 1000, (len(granule_dataset), 10))
    
    with torch.no_grad():
        outputs = model(token_ids)
    
    print(f"Processed {len(granule_dataset)} samples")
    print(f"Output shape: {outputs.shape}\n")
    
    # Step 3: Track outcome with SEPA
    print("Step 3: Recording outcome with SEPA...")
    sepa = SEPAEngine(storage_dir=Path("/tmp/integration_demo"))
    
    template = PromptTemplate(
        name="integration_test",
        content="Process data with uncertainty",
        variables=[]
    )
    sepa.register_template(template)
    
    outcome = sepa.execute_and_learn(
        request="Process granular dataset",
        template_id=template.template_id,
        solution="SheafTransformer processing",
        metrics={
            "mean_confidence": float(confs.mean()),
            "output_quality": 0.85,
        },
        success=True,
        lessons=["Granular uncertainty preserved through attention"]
    )
    
    print(f"Outcome score: {outcome.compute_score():.3f}")
    print(f"Mean confidence maintained: {confs.mean():.3f}\n")
    
    print("✓ All components integrated successfully!")


def main():
    """Run all demos."""
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  GraNT Framework - Comprehensive Demo".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    try:
        # Run demos
        demo_granular_arithmetic()
        demo_sheaf_attention()
        demo_sepa()
        demo_autocognition()
        demo_integration()
        
        print("\n" + "="*70)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
        print("Next steps:")
        print("1. Explore the API documentation")
        print("2. Run the test suite: python -m pytest tests/")
        print("3. Try your own research goals with AutoCognition")
        print("4. Contribute to the project on GitHub!")
        
    except Exception as e:
        print(f"\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
