"""
Module registry for centralized governance and component management.
Acts as a service locator and ensures all modules are compliant.
"""

import logging
from typing import Dict, Type, Optional
from .base import BaseNeuralModule, ModuleConfig

logger = logging.getLogger(__name__)


class ModuleRegistry:
    """Centralized registry for all NBOS modules"""
    
    _instance = None
    _modules: Dict[str, BaseNeuralModule] = {}
    _module_types: Dict[str, Type[BaseNeuralModule]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def register_type(cls, name: str, module_class: Type[BaseNeuralModule]) -> None:
        """Register a module type"""
        cls._module_types[name] = module_class
        logger.info(f"Registered module type: {name}")
    
    @classmethod
    def create_and_register(cls, config: ModuleConfig, module_class: Type[BaseNeuralModule]) -> BaseNeuralModule:
        """Create and register a new module instance"""
        module = module_class(config)
        cls._modules[config.name] = module
        logger.info(f"Created and registered module: {config.name}")
        return module
    
    @classmethod
    def get(cls, name: str) -> Optional[BaseNeuralModule]:
        """Retrieve a registered module"""
        return cls._modules.get(name)
    
    @classmethod
    def get_all(cls) -> Dict[str, BaseNeuralModule]:
        """Retrieve all registered modules"""
        return cls._modules.copy()
    
    @classmethod
    def unregister(cls, name: str) -> bool:
        """Unregister a module"""
        if name in cls._modules:
            del cls._modules[name]
            logger.info(f"Unregistered module: {name}")
            return True
        return False
    
    @classmethod
    def list_modules(cls) -> list:
        """List all registered modules"""
        return list(cls._modules.keys())
