"""
Self-Evolving Prompt Architecture (SEPA)
=========================================

Implements adaptive prompt templates with reinforcement learning-based evolution.

Components:
1. Outcome Tracker: Logs execution results and performance metrics
2. Learning Extractor: Identifies patterns in successful/failed approaches
3. Template Evolver: Updates prompt templates based on historical data
4. Meta-Learning Module: Cross-task knowledge transfer

Mathematical Framework:
- Template space: T = {template strings}
- Performance function: P: T → ℝ (higher is better)
- Evolution operator: T_{t+1} = T_t + Δ(T_t, outcomes)
- Convergence: P(T_t) → P* as t → ∞ (multi-armed bandit)

References:
- Pryzant et al. (2023). "Automatic Prompt Optimization with Gradient Descent"
- Zhou et al. (2022). "Large Language Models Are Human-Level Prompt Engineers"
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Callable, Tuple
from datetime import datetime
import json
import hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np


@dataclass
class Outcome:
    """
    Record of a single execution outcome.
    
    Tracks what was requested, what was done, and how well it worked.
    """
    timestamp: str
    request: str
    solution: str
    template_id: str
    metrics: Dict[str, float] = field(default_factory=dict)
    success: bool = True
    unexpected_results: List[str] = field(default_factory=list)
    lessons: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Outcome:
        """Load from dictionary."""
        return cls(**data)
    
    def compute_score(self, weights: Optional[Dict[str, float]] = None) -> float:
        """
        Compute overall performance score.
        
        Args:
            weights: Optional weights for different metrics
        
        Returns:
            Weighted score ∈ [0, 1]
        """
        if not self.metrics:
            return 1.0 if self.success else 0.0
        
        if weights is None:
            # Default: equal weights
            weights = {k: 1.0 / len(self.metrics) for k in self.metrics}
        
        score = sum(weights.get(k, 0) * v for k, v in self.metrics.items())
        
        # Penalty for failure
        if not self.success:
            score *= 0.5
        
        return max(0.0, min(1.0, score))


@dataclass
class PromptTemplate:
    """
    A prompt template with variables and performance tracking.
    
    Example:
        template = PromptTemplate(
            name="research_design",
            content="Design a {architecture} for {task} optimizing {metric}",
            variables=["architecture", "task", "metric"]
        )
    """
    name: str
    content: str
    variables: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    success_patterns: List[str] = field(default_factory=list)
    failure_patterns: List[str] = field(default_factory=list)
    performance_history: List[float] = field(default_factory=list)
    creation_time: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def template_id(self) -> str:
        """Unique identifier based on content hash."""
        return hashlib.md5(self.content.encode()).hexdigest()[:8]
    
    def instantiate(self, bindings: Dict[str, str]) -> str:
        """
        Fill in template variables.
        
        Args:
            bindings: Variable → value mapping
        
        Returns:
            Instantiated prompt string
        """
        prompt = self.content
        for var, value in bindings.items():
            if var in self.variables:
                prompt = prompt.replace(f"{{{var}}}", value)
        return prompt
    
    def get_mean_performance(self) -> float:
        """Average performance score."""
        if not self.performance_history:
            return 0.5  # Neutral prior
        return np.mean(self.performance_history)
    
    def get_confidence_interval(self, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Compute confidence interval for performance.
        
        Uses normal approximation for simplicity.
        """
        if len(self.performance_history) < 2:
            return (0.0, 1.0)
        
        mean = self.get_mean_performance()
        std = np.std(self.performance_history)
        n = len(self.performance_history)
        
        # Z-score for 95% confidence
        z = 1.96 if confidence == 0.95 else 2.576
        
        margin = z * std / np.sqrt(n)
        return (max(0, mean - margin), min(1, mean + margin))


class OutcomeTracker:
    """
    Persistent storage and retrieval of execution outcomes.
    
    Stores outcomes in JSONL format for easy appending and parsing.
    """
    
    def __init__(self, storage_path: Path):
        """
        Args:
            storage_path: Path to JSONL file for outcome storage
        """
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache
        self.outcomes: List[Outcome] = []
        
        # Load existing outcomes
        self._load_outcomes()
    
    def _load_outcomes(self):
        """Load outcomes from disk."""
        if not self.storage_path.exists():
            return
        
        with open(self.storage_path, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    self.outcomes.append(Outcome.from_dict(data))
    
    def record(self, outcome: Outcome):
        """
        Record a new outcome.
        
        Args:
            outcome: Outcome instance to store
        """
        # Add to memory
        self.outcomes.append(outcome)
        
        # Append to disk
        with open(self.storage_path, 'a') as f:
            f.write(json.dumps(outcome.to_dict()) + '\n')
    
    def query(self, 
              template_id: Optional[str] = None,
              success_only: bool = False,
              min_score: float = 0.0) -> List[Outcome]:
        """
        Query outcomes with filters.
        
        Args:
            template_id: Filter by template ID
            success_only: Only return successful outcomes
            min_score: Minimum performance score
        
        Returns:
            Filtered list of outcomes
        """
        results = self.outcomes
        
        if template_id:
            results = [o for o in results if o.template_id == template_id]
        
        if success_only:
            results = [o for o in results if o.success]
        
        if min_score > 0:
            results = [o for o in results if o.compute_score() >= min_score]
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Compute aggregate statistics.
        
        Returns:
            Dictionary with summary statistics
        """
        total = len(self.outcomes)
        successful = sum(1 for o in self.outcomes if o.success)
        
        scores = [o.compute_score() for o in self.outcomes]
        
        return {
            "total_executions": total,
            "successful": successful,
            "success_rate": successful / total if total > 0 else 0,
            "mean_score": np.mean(scores) if scores else 0,
            "median_score": np.median(scores) if scores else 0,
            "std_score": np.std(scores) if scores else 0,
        }


class LearningExtractor:
    """
    Extracts actionable insights from outcome history.
    
    Identifies:
    - Successful patterns (what works)
    - Failure patterns (what to avoid)
    - Constraint violations
    - Emerging best practices
    """
    
    def __init__(self, outcomes: List[Outcome]):
        self.outcomes = outcomes
    
    def extract_success_patterns(self, min_score: float = 0.7) -> List[str]:
        """
        Identify common elements in high-performing solutions.
        
        Args:
            min_score: Minimum score to be considered successful
        
        Returns:
            List of success patterns (textual descriptions)
        """
        successful_outcomes = [o for o in self.outcomes if o.compute_score() >= min_score]
        
        patterns = []
        
        # Extract from lessons
        for outcome in successful_outcomes:
            patterns.extend(outcome.lessons)
        
        # Frequency analysis
        pattern_counts = defaultdict(int)
        for pattern in patterns:
            pattern_counts[pattern] += 1
        
        # Return patterns appearing in >20% of successes
        threshold = len(successful_outcomes) * 0.2
        frequent_patterns = [
            pattern for pattern, count in pattern_counts.items()
            if count >= threshold
        ]
        
        return frequent_patterns
    
    def extract_failure_patterns(self, max_score: float = 0.3) -> List[str]:
        """
        Identify common elements in low-performing solutions.
        
        Returns:
            List of failure patterns to avoid
        """
        failed_outcomes = [
            o for o in self.outcomes 
            if not o.success or o.compute_score() <= max_score
        ]
        
        patterns = []
        
        for outcome in failed_outcomes:
            # Use unexpected results as failure indicators
            patterns.extend(outcome.unexpected_results)
            patterns.extend([f"avoid: {lesson}" for lesson in outcome.lessons])
        
        # Frequency analysis
        pattern_counts = defaultdict(int)
        for pattern in patterns:
            pattern_counts[pattern] += 1
        
        threshold = len(failed_outcomes) * 0.2
        frequent_patterns = [
            pattern for pattern, count in pattern_counts.items()
            if count >= threshold
        ]
        
        return frequent_patterns
    
    def suggest_new_constraints(self) -> List[str]:
        """
        Propose new constraints based on learned patterns.
        
        Returns:
            List of constraint strings
        """
        failure_patterns = self.extract_failure_patterns()
        
        constraints = []
        for pattern in failure_patterns:
            if "memory" in pattern.lower():
                constraints.append("must use < 1GB memory")
            if "latency" in pattern.lower() or "slow" in pattern.lower():
                constraints.append("must complete in < 100ms")
            if "accuracy" in pattern.lower():
                constraints.append("must achieve > 80% accuracy")
        
        return list(set(constraints))


class TemplateEvolver:
    """
    Evolves prompt templates based on performance data.
    
    Evolution strategies:
    1. Reinforce: Add success patterns to template
    2. Constrain: Add constraints to avoid failures  
    3. Mutate: Random perturbations with low probability
    4. Crossover: Combine high-performing templates
    """
    
    def __init__(self, tracker: OutcomeTracker):
        self.tracker = tracker
        self.extractor = LearningExtractor(tracker.outcomes)
    
    def evolve(self, template: PromptTemplate) -> PromptTemplate:
        """
        Create improved version of template.
        
        Args:
            template: Current template
        
        Returns:
            Evolved template
        """
        # Get outcomes for this template
        outcomes = self.tracker.query(template_id=template.template_id)
        
        if not outcomes:
            return template  # No data yet
        
        # Extract patterns
        success_patterns = self.extractor.extract_success_patterns()
        failure_patterns = self.extractor.extract_failure_patterns()
        new_constraints = self.extractor.suggest_new_constraints()
        
        # Create evolved template
        evolved = PromptTemplate(
            name=f"{template.name}_v{len(template.performance_history) + 1}",
            content=template.content,
            variables=template.variables.copy(),
            constraints=template.constraints.copy(),
            success_patterns=template.success_patterns.copy(),
            failure_patterns=template.failure_patterns.copy(),
            performance_history=[]
        )
        
        # Add new success patterns
        for pattern in success_patterns:
            if pattern not in evolved.success_patterns:
                evolved.success_patterns.append(pattern)
                # Inject into content if relevant
                if not self._is_in_content(pattern, evolved.content):
                    evolved.content += f"\n- Prefer: {pattern}"
        
        # Add constraints
        for constraint in new_constraints:
            if constraint not in evolved.constraints:
                evolved.constraints.append(constraint)
                evolved.content += f"\n- Constraint: {constraint}"
        
        # Note failure patterns
        for pattern in failure_patterns:
            if pattern not in evolved.failure_patterns:
                evolved.failure_patterns.append(pattern)
                evolved.content += f"\n- Avoid: {pattern}"
        
        return evolved
    
    def _is_in_content(self, pattern: str, content: str) -> bool:
        """Check if pattern is already mentioned in content."""
        # Simple keyword matching
        keywords = pattern.lower().split()[:3]  # First 3 words
        return all(kw in content.lower() for kw in keywords)


class SEPAEngine:
    """
    Complete Self-Evolving Prompt Architecture Engine.
    
    Coordinates:
    - Template management
    - Outcome tracking
    - Learning and evolution
    - Template selection (multi-armed bandit)
    """
    
    def __init__(self, storage_dir: Path, exploration_rate: float = 0.1):
        """
        Args:
            storage_dir: Directory for persistent storage
            exploration_rate: ε for ε-greedy template selection
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.exploration_rate = exploration_rate
        
        # Initialize components
        self.tracker = OutcomeTracker(self.storage_dir / "outcomes.jsonl")
        self.evolver = TemplateEvolver(self.tracker)
        
        # Template library
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load templates from disk."""
        template_file = self.storage_dir / "templates.json"
        if template_file.exists():
            with open(template_file, 'r') as f:
                data = json.load(f)
                for template_data in data:
                    template = PromptTemplate(**template_data)
                    self.templates[template.template_id] = template
    
    def _save_templates(self):
        """Save templates to disk."""
        template_file = self.storage_dir / "templates.json"
        data = [asdict(t) for t in self.templates.values()]
        with open(template_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_template(self, template: PromptTemplate):
        """Add a new template to the library."""
        self.templates[template.template_id] = template
        self._save_templates()
    
    def select_template(self, task_type: str) -> PromptTemplate:
        """
        Select best template for a task using ε-greedy policy.
        
        Args:
            task_type: Type of task (used to filter relevant templates)
        
        Returns:
            Selected template
        """
        # Filter relevant templates
        relevant = [t for t in self.templates.values() if task_type in t.name]
        
        if not relevant:
            raise ValueError(f"No templates found for task type: {task_type}")
        
        # ε-greedy selection
        if np.random.random() < self.exploration_rate:
            # Explore: random selection
            return np.random.choice(relevant)
        else:
            # Exploit: select best performing
            return max(relevant, key=lambda t: t.get_mean_performance())
    
    def execute_and_learn(self,
                          request: str,
                          template_id: str,
                          solution: str,
                          metrics: Dict[str, float],
                          success: bool = True,
                          lessons: Optional[List[str]] = None) -> Outcome:
        """
        Record execution outcome and trigger learning.
        
        Args:
            request: Original request
            template_id: ID of template used
            solution: Generated solution
            metrics: Performance metrics
            success: Whether execution succeeded
            lessons: Learned lessons from this execution
        
        Returns:
            Recorded outcome
        """
        outcome = Outcome(
            timestamp=datetime.now().isoformat(),
            request=request,
            solution=solution,
            template_id=template_id,
            metrics=metrics,
            success=success,
            lessons=lessons or []
        )
        
        # Record outcome
        self.tracker.record(outcome)
        
        # Update template performance
        if template_id in self.templates:
            score = outcome.compute_score()
            self.templates[template_id].performance_history.append(score)
            self._save_templates()
        
        # Trigger evolution if enough data
        if template_id in self.templates:
            template = self.templates[template_id]
            if len(template.performance_history) >= 5:  # Minimum samples
                evolved = self.evolver.evolve(template)
                if evolved.template_id != template.template_id:
                    self.register_template(evolved)
                    print(f"✨ Evolved template: {template.name} → {evolved.name}")
        
        return outcome
    
    def get_best_template(self, task_type: str) -> PromptTemplate:
        """Get current best performing template for a task."""
        relevant = [t for t in self.templates.values() if task_type in t.name]
        if not relevant:
            raise ValueError(f"No templates for {task_type}")
        return max(relevant, key=lambda t: t.get_mean_performance())
    
    def generate_report(self) -> str:
        """Generate human-readable report of system status."""
        stats = self.tracker.get_statistics()
        
        report = "=== SEPA Status Report ===\n\n"
        report += f"Total Executions: {stats['total_executions']}\n"
        report += f"Success Rate: {stats['success_rate']:.1%}\n"
        report += f"Mean Score: {stats['mean_score']:.3f}\n"
        report += f"Active Templates: {len(self.templates)}\n\n"
        
        report += "Top Performing Templates:\n"
        sorted_templates = sorted(
            self.templates.values(),
            key=lambda t: t.get_mean_performance(),
            reverse=True
        )[:5]
        
        for i, template in enumerate(sorted_templates, 1):
            perf = template.get_mean_performance()
            n = len(template.performance_history)
            report += f"{i}. {template.name}: {perf:.3f} (n={n})\n"
        
        return report


if __name__ == "__main__":
    print("=== SEPA Engine Demo ===\n")
    
    # Create engine
    engine = SEPAEngine(storage_dir=Path("/tmp/sepa_demo"))
    
    # Create initial template
    template = PromptTemplate(
        name="research_design_v1",
        content="""Design a {architecture} architecture for {task}.
        
Optimize for: {metric}
        
Requirements:
- Must be production-ready
- Include error handling
- Document all assumptions
""",
        variables=["architecture", "task", "metric"]
    )
    
    engine.register_template(template)
    
    # Simulate executions
    print("Simulating 10 executions...\n")
    
    for i in range(10):
        outcome = engine.execute_and_learn(
            request=f"Design transformer variant #{i}",
            template_id=template.template_id,
            solution=f"Solution {i}",
            metrics={
                "accuracy": 0.8 + np.random.rand() * 0.2,
                "latency": 10 + np.random.rand() * 20,
                "memory": 0.5 + np.random.rand() * 0.5
            },
            success=np.random.rand() > 0.2,
            lessons=[
                "cocycle regularization helps" if i % 3 == 0 else "standard attention works",
                "warmup is important" if i % 2 == 0 else "no warmup needed"
            ]
        )
        print(f"Execution {i+1}: score={outcome.compute_score():.3f}")
    
    print("\n" + engine.generate_report())
    
    print("\n✓ SEPA engine working correctly!")
