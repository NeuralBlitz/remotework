"""Workflow automation and self-evolving systems."""

from grant.workflows.sepa import (
    Outcome,
    PromptTemplate,
    OutcomeTracker,
    LearningExtractor,
    TemplateEvolver,
    SEPAEngine,
)

from grant.workflows.auto_cognition import (
    ResearchGoal,
    Solution,
    AutoCognitionEngine,
)

__all__ = [
    "Outcome",
    "PromptTemplate",
    "OutcomeTracker",
    "LearningExtractor",
    "TemplateEvolver",
    "SEPAEngine",
    "ResearchGoal",
    "Solution",
    "AutoCognitionEngine",
]
