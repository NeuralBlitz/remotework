"""
GraNT Test Suite
================

Comprehensive tests for all components:
- Granular arithmetic
- Sheaf attention
- SEPA workflow
- AutoCognition engine
"""

import unittest
import tempfile
from pathlib import Path
import torch
import numpy as np
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.granule import Granule, GranuleSpace, make_granule, GranuleType
from core.sheaf_attention import (
    Poset, CocycleAttention, SheafAttentionLayer, 
    SheafTransformer, create_hierarchical_poset
)
from workflows.sepa import (
    Outcome, PromptTemplate, OutcomeTracker, 
    LearningExtractor, TemplateEvolver, SEPAEngine
)
from workflows.auto_cognition import AutoCognitionEngine, ResearchGoal


class TestGranularArithmetic(unittest.TestCase):
    """Test granular arithmetic operations."""
    
    def test_granule_creation(self):
        """Test basic granule creation."""
        g = make_granule([1.0, 2.0, 3.0], confidence=0.9)
        
        self.assertEqual(g.dtype, GranuleType.VECTOR)
        self.assertEqual(g.confidence, 0.9)
        np.testing.assert_array_equal(g.value, np.array([1.0, 2.0, 3.0]))
    
    def test_granule_addition(self):
        """Test granular addition operator."""
        g1 = make_granule([1.0, 2.0], confidence=0.9)
        g2 = make_granule([0.5, 0.5], confidence=0.8)
        
        g3 = g1 + g2
        
        np.testing.assert_array_almost_equal(g3.value, np.array([1.5, 2.5]))
        self.assertEqual(g3.confidence, 0.8)  # min(0.9, 0.8)
    
    def test_granule_fusion(self):
        """Test granular fusion operator."""
        g1 = make_granule([1.0, 2.0], confidence=0.9)
        g2 = make_granule([3.0, 4.0], confidence=0.8)
        
        g3 = g1.fuse(g2)
        
        self.assertEqual(len(g3.value), 4)  # Concatenation
        self.assertAlmostEqual(g3.confidence, 0.72, places=2)  # 0.9 * 0.8
    
    def test_granule_projection(self):
        """Test uncertainty propagation in projections."""
        g = make_granule([3.0, 4.0], confidence=0.9)
        
        # Normalize (Lipschitz constant ~ 1)
        def normalize(x):
            return x / (np.linalg.norm(x) + 1e-10)
        
        g_proj = g.project(normalize, lipschitz_constant=1.0)
        
        # Confidence should decrease slightly
        self.assertLess(g_proj.confidence, g.confidence)
        
        # Value should be normalized
        self.assertAlmostEqual(np.linalg.norm(g_proj.value), 1.0, places=5)
    
    def test_granule_space_aggregation(self):
        """Test aggregation of granule spaces."""
        granules = [
            make_granule([1.0], confidence=0.9),
            make_granule([2.0], confidence=0.8),
            make_granule([3.0], confidence=0.7)
        ]
        space = GranuleSpace(granules)
        
        agg = space.aggregate(method="mean")
        
        # Weighted mean should be closer to high-confidence values
        self.assertGreater(agg.value[0], 1.5)
        self.assertLess(agg.value[0], 2.5)
    
    def test_tensor_conversion(self):
        """Test conversion to PyTorch tensors."""
        g = make_granule([1.0, 2.0, 3.0])
        tensor = g.to_tensor()
        
        self.assertIsInstance(tensor, torch.Tensor)
        self.assertEqual(tensor.shape, (3,))


class TestSheafAttention(unittest.TestCase):
    """Test sheaf-theoretic attention mechanisms."""
    
    def test_poset_creation(self):
        """Test poset structure."""
        poset = create_hierarchical_poset([512, 64, 8])
        
        self.assertEqual(len(poset.elements), 3)
        self.assertTrue(poset.is_leq(0, 2))  # Transitivity
        self.assertFalse(poset.is_leq(2, 0))  # Anti-symmetry
    
    def test_cocycle_attention_forward(self):
        """Test cocycle attention computation."""
        d_model = 64
        batch_size = 2
        seq_len = 10
        
        attn = CocycleAttention(d_model=d_model, temperature=1.0)
        
        Q = torch.randn(batch_size, seq_len, d_model)
        K = torch.randn(batch_size, seq_len, d_model)
        V = torch.randn(batch_size, seq_len, d_model)
        
        output, weights = attn(Q, K, V)
        
        # Check shapes
        self.assertEqual(output.shape, (batch_size, seq_len, d_model))
        self.assertEqual(weights.shape, (batch_size, seq_len, seq_len))
        
        # Check attention normalization (should sum to 1)
        weight_sums = weights.sum(dim=-1)
        np.testing.assert_array_almost_equal(
            weight_sums.detach().numpy(), 
            np.ones((batch_size, seq_len)), 
            decimal=5
        )
    
    def test_sheaf_attention_layer(self):
        """Test complete sheaf attention layer."""
        d_model = 128
        n_heads = 4
        batch_size = 2
        seq_len = 16
        
        layer = SheafAttentionLayer(d_model=d_model, n_heads=n_heads)
        
        x = torch.randn(batch_size, seq_len, d_model)
        output = layer(x)
        
        # Shape preservation
        self.assertEqual(output.shape, x.shape)
        
        # No NaN or Inf
        self.assertFalse(torch.isnan(output).any())
        self.assertFalse(torch.isinf(output).any())
    
    def test_sheaf_transformer(self):
        """Test full SheafTransformer."""
        vocab_size = 1000
        d_model = 128
        n_layers = 2
        batch_size = 2
        seq_len = 32
        
        model = SheafTransformer(
            vocab_size=vocab_size,
            d_model=d_model,
            n_layers=n_layers
        )
        
        input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
        logits = model(input_ids)
        
        self.assertEqual(logits.shape, (batch_size, seq_len, vocab_size))
        
        # Check valid probability distribution
        probs = torch.softmax(logits, dim=-1)
        self.assertTrue((probs >= 0).all())
        self.assertTrue((probs <= 1).all())


class TestSEPA(unittest.TestCase):
    """Test Self-Evolving Prompt Architecture."""
    
    def setUp(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_outcome_creation(self):
        """Test outcome recording."""
        outcome = Outcome(
            timestamp="2026-01-20T10:00:00",
            request="Test request",
            solution="Test solution",
            template_id="abc123",
            metrics={"accuracy": 0.9, "latency": 10.5},
            success=True,
            lessons=["Lesson 1", "Lesson 2"]
        )
        
        score = outcome.compute_score()
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 1)
    
    def test_outcome_tracker(self):
        """Test outcome tracking and querying."""
        tracker = OutcomeTracker(Path(self.temp_dir) / "outcomes.jsonl")
        
        # Record outcomes
        for i in range(5):
            outcome = Outcome(
                timestamp=f"2026-01-20T10:00:{i:02d}",
                request=f"Request {i}",
                solution=f"Solution {i}",
                template_id="template_v1",
                metrics={"score": 0.5 + i * 0.1},
                success=True
            )
            tracker.record(outcome)
        
        # Query
        all_outcomes = tracker.query()
        self.assertEqual(len(all_outcomes), 5)
        
        successful = tracker.query(success_only=True)
        self.assertEqual(len(successful), 5)
        
        high_score = tracker.query(min_score=0.8)
        self.assertGreater(len(high_score), 0)
    
    def test_template_evolution(self):
        """Test template evolution."""
        template = PromptTemplate(
            name="test_template",
            content="Original content",
            variables=["var1", "var2"]
        )
        
        # Simulate performance history
        template.performance_history = [0.6, 0.7, 0.8]
        
        # Template should report good performance
        mean_perf = template.get_mean_performance()
        self.assertGreater(mean_perf, 0.6)
    
    def test_sepa_engine(self):
        """Test complete SEPA engine."""
        engine = SEPAEngine(storage_dir=Path(self.temp_dir), exploration_rate=0.1)
        
        # Register template
        template = PromptTemplate(
            name="test_design_v1",
            content="Design {component}",
            variables=["component"]
        )
        engine.register_template(template)
        
        # Execute and learn
        outcome = engine.execute_and_learn(
            request="Design transformer",
            template_id=template.template_id,
            solution="class Transformer(...)",
            metrics={"accuracy": 0.85},
            success=True,
            lessons=["Attention is key"]
        )
        
        self.assertIsInstance(outcome, Outcome)
        
        # Check template was updated
        updated_template = engine.templates[template.template_id]
        self.assertEqual(len(updated_template.performance_history), 1)


class TestAutoCognition(unittest.TestCase):
    """Test AutoCognition engine."""
    
    def setUp(self):
        """Create engine instance."""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = AutoCognitionEngine(
            storage_dir=Path(self.temp_dir),
            enable_gpu=False
        )
    
    def test_task_classification(self):
        """Test task type classification."""
        task1 = "Design a transformer architecture"
        task2 = "Prove that attention converges"
        task3 = "Optimize the model for latency"
        
        self.assertEqual(self.engine._classify_task(task1), "architecture_design")
        self.assertEqual(self.engine._classify_task(task2), "mathematical_proof")
        self.assertEqual(self.engine._classify_task(task3), "optimization")
    
    def test_solution_generation(self):
        """Test solution generation."""
        goal = ResearchGoal(
            description="Design low-latency attention",
            constraints={"latency_ms": 10, "memory_mb": 1},
            metrics=["latency", "memory"],
            context={}
        )
        
        # Get template
        template = self.engine.sepa.select_template("architecture_design")
        
        # Generate solution
        solution = self.engine._generate_solution(goal, template)
        
        self.assertIsNotNone(solution.architecture)
        self.assertIsInstance(solution.architecture, torch.nn.Module)
        self.assertIn("SheafTransformer", solution.code)
    
    def test_full_investigation(self):
        """Test complete investigation workflow."""
        goal = ResearchGoal(
            description="Design efficient attention mechanism",
            constraints={"latency_ms": 20, "memory_mb": 5},
            metrics=["accuracy", "latency", "memory"],
            context={"team_size": 2}
        )
        
        solution = self.engine.investigate(goal)
        
        self.assertIsNotNone(solution)
        self.assertIsNotNone(solution.architecture)
        self.assertIsNotNone(solution.documentation)
        self.assertIsNotNone(solution.proof_trace)


class TestIntegration(unittest.TestCase):
    """Integration tests across components."""
    
    def test_granule_to_sheaf(self):
        """Test using granules with sheaf attention."""
        # Create granule space
        granules = [make_granule(np.random.randn(64), confidence=0.9) for _ in range(10)]
        space = GranuleSpace(granules)
        
        # Convert to tensor batch
        values, confidences = space.to_tensor_batch()
        
        # Pass through sheaf attention
        attn = CocycleAttention(d_model=64)
        output, weights = attn(values.unsqueeze(0), values.unsqueeze(0), values.unsqueeze(0))
        
        self.assertEqual(output.shape, (1, 10, 64))
        
        # Weights should respect confidence
        # (high confidence items should attend more)
        high_conf_idx = confidences.argmax()
        self.assertGreater(weights[0, :, high_conf_idx].mean(), 0.05)


def run_all_tests():
    """Run all test suites."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestGranularArithmetic))
    suite.addTests(loader.loadTestsFromTestCase(TestSheafAttention))
    suite.addTests(loader.loadTestsFromTestCase(TestSEPA))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoCognition))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("="*70)
    print("GraNT Test Suite")
    print("="*70)
    print()
    
    success = run_all_tests()
    
    print()
    print("="*70)
    if success:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*70)
    
    exit(0 if success else 1)
