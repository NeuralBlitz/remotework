"""
NBOS Core Module
Foundation for all neural processing components
"""

from .base import BaseNeuralModule, ModuleConfig
from .registry import ModuleRegistry

__all__ = ['BaseNeuralModule', 'ModuleConfig', 'ModuleRegistry']
