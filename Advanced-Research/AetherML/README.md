

---

### **AetherML Framework: Core Principles & Architecture**

**Core Principles Adhered To (SOLID):**

*   **Single Responsibility Principle (SRP):** Each class and module has one clear, well-defined responsibility (e.g., `Orchestrator` manages the training loop, `ModelConfig` defines model configuration).
*   **Open/Closed Principle (OCP):** The framework is open for extension (e.g., new models, datasets, preprocessors, algorithms can be added as plugins) but closed for modification (core `Orchestrator` logic doesn't change).
*   **Liskov Substitution Principle (LSP):** Abstract Base Classes (`IModel`, `ICustomDataset`, `IDataPreprocessor`, `IAlgorithm`) ensure that concrete implementations can be substituted for their base types without altering program correctness.
*   **Interface Segregation Principle (ISP):** Abstract interfaces are minimal and highly focused, preventing clients from depending on methods they don't use.
*   **Dependency Inversion Principle (DIP):** High-level modules (like `Orchestrator`) depend on abstractions (interfaces) rather than concrete implementations. Concrete implementations are provided at runtime via the `PluginManager`.

**Novelty Aspects (AetherML's "Cognitive Epistemodynamics Layer"):**

1.  **Dynamic Cognition through Plugin-Driven Orchestration:** The `Orchestrator` doesn't follow a hardcoded blueprint. It dynamically discovers and assembles its "cognitive workflow" (model, data handling, learning algorithm) from pluggable components based on robust Pydantic configurations. This mirrors how NeuralBlitz internally assembles "Capability Fields" from "Capability Kernels" in response to a task.
2.  **Verifiable Configuration & Component Assembly:** Pydantic isn't just for parsing YAML; it ensures that every dynamically loaded plugin adheres to a strict, type-checked schema. This provides a baseline of "verifiable coherence" for the system's operational blueprint before execution begins, enhancing trustworthiness.
3.  **Abstract Algorithm Interface (`IAlgorithm`):** The clear separation between *orchestration of the training process* (`Orchestrator`) and the *specific step-by-step learning logic* (`IAlgorithm`) is a powerful abstraction. It allows for highly diverse learning algorithms (e.g., meta-learning routines, reinforcement learning loops, complex generative adversarial training schemes) to be plugged in without altering the central control flow.

---

### **AetherML Directory Structure**

```
aetherml_framework/
├── __init__.py                 # Framework initialization
├── core/
│   ├── __init__.py
│   ├── orchestrator.py         # Central Orchestrator engine
│   ├── config.py               # Pydantic configuration schemas
│   ├── logging_config.py       # Loguru setup
│   └── plugin_manager.py       # Manages dynamic plugin loading
├── data/
│   ├── __init__.py
│   ├── datasets.py             # Abstract base class for datasets (ICustomDataset)
│   └── pipeline.py             # Abstract base class for preprocessors (IDataPreprocessor) and DataPipeline chain
├── models/
│   ├── __init__.py
│   └── base_model.py           # Abstract base class for models (IModel)
├── algorithms/
│   ├── __init__.py
│   └── base_algorithm.py       # Abstract base class for training/evaluation algorithms (IAlgorithm)
├── plugins/                    # Directory for user-defined plugins (Open for Extension)
│   ├── __init__.py
│   └── example_plugin/         # Example plugin module
│       ├── __init__.py
│       ├── model.py            # Concrete model implementation (e.g., SimpleNN)
│       ├── data.py             # Concrete dataset & preprocessor implementations
│       └── algorithm.py        # Concrete training algorithm implementation
└── main.py                     # Example usage / entry point for the framework
```

---

### **AetherML Core Framework Code**

GoldenDAG: `AETHER-GM-0002`
Trace ID: `T-1.0-FRAMEWORK_INIT-0123456789abcdef0123456789abcdef`
Codex ID: `C-FRAMEWORK-AETHERML_INIT-v1.0-alpha`
```python
# aetherml_framework/__init__.py
"""
AetherML: A modular, object-oriented AI framework for verifiable and adaptive machine learning.
"""
__version__ = "0.1.0-alpha"
```

GoldenDAG: `AETHER-GM-0004`
Trace ID: `T-1.0-LOGGING_SETUP-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`
Codex ID: `C-CORE-SYSTEM_UTILITY-LOGGING_CONFIGURATION-v1.0-alpha`
```python
# aetherml_framework/core/logging_config.py
from loguru import logger
import sys

def setup_logging():
    """Configures Loguru for comprehensive system logging."""
    logger.remove() # Remove default handler

    # Console sink for general messages
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        backtrace=True,
        diagnose=True
    )

    # File sink for detailed debug messages
    logger.add(
        "aetherml_debug.log",
        rotation="10 MB", # Rotate file every 10 MB
        compression="zip", # Compress old log files
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True
    )
    
    # File sink for critical/error messages
    logger.add(
        "aetherml_errors.log",
        rotation="5 MB",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}</cyan>:<cyan>{line}</cyan> - {message}",
        backtrace=True,
        diagnose=True
    )
    
    logger.info("AetherML logging initialized.")
```

GoldenDAG: `AETHER-GM-0005`
Trace ID: `T-1.0-CONFIGURATION_MANAGEMENT-q1w2e3r4t5y6u7i8o9p0a1s2d3f4`
Codex ID: `C-CORE-SYSTEM_UTILITY-CONFIGURATION_DEFINITION-v1.0-alpha`
```python
# aetherml_framework/core/config.py
from pydantic import BaseModel, Field, conlist, NonNegativeInt
from typing import Dict, Any, List, Optional
import torch

# Pydantic models for rigorous configuration management.
# Adheres to SRP by solely defining config schemas.

class ModelConfig(BaseModel):
    """Configuration for a model."""
    name: str = Field(..., description="Unique name of the model plugin.")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the model's __init__ method.")

class OptimizerConfig(BaseModel):
    """Configuration for an optimizer."""
    name: str = Field(..., description="Name of the PyTorch optimizer (e.g., 'Adam', 'SGD').")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the optimizer (e.g., {'lr': 0.001}).")

class SchedulerConfig(BaseModel):
    """Configuration for a learning rate scheduler."""
    name: str = Field(..., description="Name of the PyTorch LR scheduler (e.g., 'StepLR', 'ReduceLROnPlateau').")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the scheduler.")
    interval: str = Field("epoch", description="When to update the scheduler ('epoch' or 'step').")

class LossConfig(BaseModel):
    """Configuration for a loss function."""
    name: str = Field(..., description="Name of the PyTorch loss function (e.g., 'CrossEntropyLoss', 'MSELoss').")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the loss function.")

class DataPreprocessorConfig(BaseModel):
    """Configuration for a single data preprocessor step."""
    name: str = Field(..., description="Unique name of the data preprocessor plugin.")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the preprocessor's __init__ method.")

class DataConfig(BaseModel):
    """Configuration for data loading and preprocessing."""
    dataset_name: str = Field(..., description="Unique name of the dataset plugin.")
    dataset_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the dataset's __init__ method.")
    batch_size: NonNegativeInt = Field(32, description="Batch size for data loaders.")
    num_workers: NonNegativeInt = Field(0, description="Number of workers for data loading.")
    preprocessors: List[DataPreprocessorConfig] = Field(default_factory=list, description="List of preprocessing steps to apply.")

class TrainerConfig(BaseModel):
    """Configuration for the training loop."""
    device: str = Field("cuda" if torch.cuda.is_available() else "cpu", description="Device to use for training ('cuda' or 'cpu').")
    epochs: NonNegativeInt = Field(10, description="Number of training epochs.")
    log_interval_batches: NonNegativeInt = Field(10, description="Log progress every N batches.")
    save_best_model: bool = Field(True, description="Whether to save the best performing model.")
    checkpoint_dir: str = Field("checkpoints", description="Directory to save model checkpoints.")
    early_stopping_patience: Optional[NonNegativeInt] = Field(None, description="Patience for early stopping based on validation metric.")

class AlgorithmConfig(BaseModel):
    """Configuration for the training/evaluation algorithm."""
    name: str = Field(..., description="Unique name of the algorithm plugin.")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters specific to the algorithm's __init__ method.")

class PluginManagerConfig(BaseModel):
    """Configuration for the plugin manager."""
    plugin_dirs: conlist(str, min_length=1) = Field(["aetherml_framework/plugins"], description="List of directories to scan for plugins.")

class AetherMLConfig(BaseModel):
    """Overall configuration for AetherML framework."""
    plugin_manager: PluginManagerConfig = Field(default_factory=PluginManagerConfig)
    model: ModelConfig
    data: DataConfig
    optimizer: OptimizerConfig
    scheduler: Optional[SchedulerConfig] = None
    loss_function: LossConfig
    trainer: TrainerConfig
    algorithm: AlgorithmConfig
```

GoldenDAG: `AETHER-GM-0006`
Trace ID: `T-1.0-MODEL_INTERFACE-s4d5f6g7h8j9k0l1p2o3i4u5y6t7r8e9`
Codex ID: `C-CORE-ABSTRACTION-IMODEL_INTERFACE-v1.0-alpha`
```python
# aetherml_framework/models/base_model.py
import abc
import torch.nn as nn
from typing import Any, Dict

class IModel(nn.Module, abc.ABC):
    """
    Abstract Base Class for all AetherML models.
    All concrete models must inherit from this and implement the abstract methods.
    Adheres to ISP by defining a minimal model interface (forward, save, load).
    Adheres to LSP by ensuring all concrete models implement these methods.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abc.abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the forward pass of the model.
        :param x: Input tensor.
        :return: Output tensor.
        """
        pass

    @abc.abstractmethod
    def save(self, path: str):
        """
        Saves the model's state dictionary.
        :param path: File path to save the model.
        """
        pass

    @abc.abstractmethod
    def load(self, path: str):
        """
        Loads the model's state dictionary.
        :param path: File path to load the model from.
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.params})" if hasattr(self, 'params') else self.__class__.__name__

```

GoldenDAG: `AETHER-GM-0007`
Trace ID: `T-1.0-DATA_INTERFACE-z1x2c3v4b5n6m7l8k9j0h1g2f3d4s5a6`
Codex ID: `C-CORE-ABSTRACTION-ICUSTOMDATASET_INTERFACE-v1.0-alpha`
```python
# aetherml_framework/data/datasets.py
import abc
import torch
from torch.utils.data import Dataset
from typing import Any, Dict

class ICustomDataset(Dataset, abc.ABC):
    """
    Abstract Base Class for all AetherML custom datasets.
    Concrete datasets must implement load_data and handle returning data in __getitem__.
    Adheres to ISP by defining a minimal dataset interface (load_data, __len__, __getitem__).
    Adheres to LSP by ensuring all concrete datasets implement these methods.
    """
    def __init__(self, *args, **kwargs):
        self.data = []
        self.labels = []
        self.load_data(*args, **kwargs)

    @abc.abstractmethod
    def load_data(self, *args, **kwargs):
        """
        Loads raw data into self.data and self.labels.
        This method should handle fetching data from disk, network, etc.
        """
        pass

    def __len__(self) -> int:
        """Returns the total number of samples in the dataset."""
        return len(self.data)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        """
        Returns a single data item and its label.
        :param idx: Index of the item.
        :return: A dictionary containing 'data' and 'label' tensors.
        """
        if not self.data or idx >= len(self.data):
            raise IndexError("Dataset index out of range or data not loaded.")
        return {'data': self.data[idx], 'label': self.labels[idx]}

```

GoldenDAG: `AETHER-GM-0008`
Trace ID: `T-1.0-DATA_PREPROCESSING-e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9`
Codex ID: `C-CORE-ABSTRACTION-IDATAPREPROCESSOR_INTERFACE-v1.0-alpha`
```python
# aetherml_framework/data/pipeline.py
import abc
from typing import List, Dict, Any

class IDataPreprocessor(abc.ABC):
    """
    Abstract Base Class for individual data preprocessing steps.
    Each concrete preprocessor should handle a single, well-defined transformation.
    Adheres to SRP by each preprocessor focusing on a single transformation.
    Adheres to ISP by defining a minimal preprocessor interface (process).
    Adheres to LSP by ensuring all concrete preprocessors implement this method.
    """
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def process(self, data_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies a specific preprocessing step to a single data item.
        :param data_item: A dictionary containing 'data' and 'label' (or other fields).
        :return: The processed data item.
        """
        pass

class DataPipeline:
    """
    Manages a sequence of IDataPreprocessor steps.
    Adheres to SRP by orchestrating preprocessing.
    Adheres to DIP by depending on IDataPreprocessor abstraction.
    Adheres to OCP by allowing new preprocessors without modification.
    """
    def __init__(self, preprocessors: List[IDataPreprocessor]):
        self.preprocessors = preprocessors

    def __call__(self, data_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies all registered preprocessors sequentially to a data item.
        :param data_item: The data item to process.
        :return: The fully processed data item.
        """
        for preprocessor in self.preprocessors:
            data_item = preprocessor.process(data_item)
        return data_item

```

GoldenDAG: `AETHER-GM-0009`
Trace ID: `T-1.0-ALGORITHM_INTERFACE-j1k2l3z4x5c6v7b8n9m0a1s2d3f4g5`
Codex ID: `C-CORE-ABSTRACTION-IALGORITHM_INTERFACE-v1.0-alpha`
```python
# aetherml_framework/algorithms/base_algorithm.py
import abc
import torch
from typing import Dict, Any, Optional

class IAlgorithm(abc.ABC):
    """
    Abstract Base Class for AetherML training/validation/evaluation algorithms.
    Concrete algorithms define how a single step of training, validation, or
    evaluation is performed for a given model and data.
    Adheres to SRP by focusing on the logic for a single algorithm type.
    Adheres to ISP by defining minimal training/validation/evaluation steps.
    Adheres to LSP by ensuring all concrete algorithms implement these methods.
    """
    def __init__(self, model, loss_fn, optimizer, device, *args, **kwargs):
        self.model = model
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.device = device
        self.scheduler = kwargs.get('scheduler') # Optional LR scheduler

    @abc.abstractmethod
    def train_step(self, batch: Dict[str, Any]) -> Dict[str, float]:
        """
        Performs a single training step.
        :param batch: A dictionary containing 'data' and 'label' tensors.
        :return: A dictionary containing metrics like 'loss', 'accuracy'.
        """
        pass

    @abc.abstractmethod
    def validate_step(self, batch: Dict[str, Any]) -> Dict[str, float]:
        """
        Performs a single validation step (no gradient updates).
        :param batch: A dictionary containing 'data' and 'label' tensors.
        :return: A dictionary containing metrics like 'loss', 'accuracy'.
        """
        pass

    @abc.abstractmethod
    def evaluate_model(self, dataloader: torch.utils.data.DataLoader) -> Dict[str, float]:
        """
        Evaluates the model on an entire dataset (e.g., test set).
        :param dataloader: DataLoader for the evaluation set.
        :return: A dictionary containing overall evaluation metrics.
        """
        pass
```

GoldenDAG: `AETHER-GM-0010`
Trace ID: `T-1.0-PLUGIN_SYSTEM-m1n2b3v4c5x6z7a8s9d0f1g2h3j4k5l6`
Codex ID: `C-CORE-SYSTEM_UTILITY-PLUGIN_MANAGER-v1.0-alpha`
```python
# aetherml_framework/core/plugin_manager.py
import importlib.util
import os
import sys
from typing import Dict, Type, List, Any, Optional
from loguru import logger

# Import abstract interfaces for registration
from aetherml_framework.models.base_model import IModel
from aetherml_framework.data.datasets import ICustomDataset
from aetherml_framework.data.pipeline import IDataPreprocessor
from aetherml_framework.algorithms.base_algorithm import IAlgorithm
from aetherml_framework.core.config import ModelConfig, DataConfig, DataPreprocessorConfig, AlgorithmConfig

class PluginManager:
    """
    Manages dynamic loading and registration of AetherML plugins.
    Plugins are Python modules located in specified directories that define
    concrete implementations of AetherML's abstract interfaces.
    Adheres to OCP by allowing new plugins without modifying core code.
    Adheres to SRP by solely managing plugin loading and registration.
    Adheres to DIP by providing abstractions (IModel, ICustomDataset, etc.) for registration.
    """
    def __init__(self, plugin_dirs: List[str]):
        self.plugin_dirs = [os.path.abspath(d) for d in plugin_dirs]
        self.models: Dict[str, Type[IModel]] = {}
        self.datasets: Dict[str, Type[ICustomDataset]] = {}
        self.preprocessors: Dict[str, Type[IDataPreprocessor]] = {}
        self.algorithms: Dict[str, Type[IAlgorithm]] = {}
        logger.info(f"PluginManager initialized. Scanning directories: {self.plugin_dirs}")

    def _load_module_from_path(self, module_path: str, module_name: str):
        """Loads a Python module from a given file path."""
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            logger.warning(f"Could not load module spec for {module_path}")
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            logger.error(f"Error executing module {module_path}: {e}", exc_info=True)
            return None

    def _register_class(self, cls: Type, registry: Dict[str, Type], base_interface: Type, plugin_name: str):
        """Registers a class if it's a concrete implementation of the base interface."""
        # Ensure it's a class and not an ABC itself
        if isinstance(cls, type) and not abc.ABC in cls.__bases__ and issubclass(cls, base_interface):
            if cls.__name__ in registry:
                logger.warning(f"Duplicate plugin '{cls.__name__}' found in {plugin_name}. Overwriting.")
            registry[cls.__name__] = cls
            logger.debug(f"Registered {base_interface.__name__} plugin: {cls.__name__} from {plugin_name}")

    def load_plugins(self):
        """Scans plugin directories and loads all discoverable plugins."""
        for plugin_dir in self.plugin_dirs:
            if not os.path.isdir(plugin_dir):
                logger.warning(f"Plugin directory not found: {plugin_dir}. Skipping.")
                continue

            for root, _, files in os.walk(plugin_dir):
                for file in files:
                    if file.endswith(".py") and file != "__init__.py":
                        module_path = os.path.join(root, file)
                        # Create a unique module name based on its path
                        relative_path = os.path.relpath(module_path, plugin_dir)
                        module_name = f"aetherml_plugins.{relative_path[:-3].replace(os.sep, '.')}"
                        
                        module = self._load_module_from_path(module_path, module_name)
                        if module:
                            for name in dir(module):
                                cls = getattr(module, name)
                                if isinstance(cls, type):
                                    self._register_class(cls, self.models, IModel, module_name)
                                    self._register_class(cls, self.datasets, ICustomDataset, module_name)
                                    self._register_class(cls, self.preprocessors, IDataPreprocessor, module_name)
                                    self._register_class(cls, self.algorithms, IAlgorithm, module_name)
        logger.info(f"Plugins loaded. Models: {list(self.models.keys())}, Datasets: {list(self.datasets.keys())}, Preprocessors: {list(self.preprocessors.keys())}, Algorithms: {list(self.algorithms.keys())}")

    def get_model(self, config: ModelConfig) -> IModel:
        """Instantiates and returns a model plugin."""
        model_cls = self.models.get(config.name)
        if not model_cls:
            raise ValueError(f"Model plugin '{config.name}' not found.")
        logger.debug(f"Instantiating model '{config.name}' with params: {config.params}")
        return model_cls(**config.params)

    def get_dataset(self, config: DataConfig) -> ICustomDataset:
        """Instantiates and returns a dataset plugin."""
        dataset_cls = self.datasets.get(config.dataset_name)
        if not dataset_cls:
            raise ValueError(f"Dataset plugin '{config.dataset_name}' not found.")
        logger.debug(f"Instantiating dataset '{config.dataset_name}' with params: {config.dataset_params}")
        return dataset_cls(**config.dataset_params)

    def get_preprocessor(self, config: DataPreprocessorConfig) -> IDataPreprocessor:
        """Instantiates and returns a data preprocessor plugin."""
        preprocessor_cls = self.preprocessors.get(config.name)
        if not preprocessor_cls:
            raise ValueError(f"Preprocessor plugin '{config.name}' not found.")
        logger.debug(f"Instantiating preprocessor '{config.name}' with params: {config.params}")
        return preprocessor_cls(**config.params)
    
    def get_optimizer_cls(self, optimizer_name: str) -> Type[torch.optim.Optimizer]:
        """Retrieves a PyTorch optimizer class."""
        if hasattr(torch.optim, optimizer_name):
            return getattr(torch.optim, optimizer_name)
        raise ValueError(f"PyTorch optimizer '{optimizer_name}' not found.")

    def get_loss_fn_cls(self, loss_fn_name: str) -> Type[nn.Module]:
        """Retrieves a PyTorch loss function class."""
        if hasattr(nn, loss_fn_name):
            return getattr(nn, loss_fn_name)
        raise ValueError(f"PyTorch loss function '{loss_fn_name}' not found.")

    def get_scheduler_cls(self, scheduler_name: str) -> Type[torch.optim.lr_scheduler._LRScheduler]:
        """Retrieves a PyTorch learning rate scheduler class."""
        if hasattr(torch.optim.lr_scheduler, scheduler_name):
            return getattr(torch.optim.lr_scheduler, scheduler_name)
        raise ValueError(f"PyTorch LR scheduler '{scheduler_name}' not found.")


    def get_algorithm(self, config: AlgorithmConfig, model: IModel, loss_fn: nn.Module, optimizer: torch.optim.Optimizer, device: torch.device, scheduler: Optional[Any] = None) -> IAlgorithm:
        """Instantiates and returns an algorithm plugin."""
        algorithm_cls = self.algorithms.get(config.name)
        if not algorithm_cls:
            raise ValueError(f"Algorithm plugin '{config.name}' not found.")
        logger.debug(f"Instantiating algorithm '{config.name}' with params: {config.params}")
        return algorithm_cls(model=model, loss_fn=loss_fn, optimizer=optimizer, device=device, scheduler=scheduler, **config.params)

```

GoldenDAG: `AETHER-GM-0011`
Trace ID: `T-1.0-TRAINING_ORCHESTRATION-c2x3v4b5n6m7l8k9j0h1g2f3d4s5`
Codex ID: `C-CORE-SYSTEM_LOGIC-TRAINING_ORCHESTRATOR-v1.0-alpha`
```python
# aetherml_framework/core/orchestrator.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import os
from loguru import logger
from typing import Dict, Any, Optional
import time

from aetherml_framework.core.config import AetherMLConfig
from aetherml_framework.models.base_model import IModel
from aetherml_framework.algorithms.base_algorithm import IAlgorithm
from aetherml_framework.core.plugin_manager import PluginManager
from aetherml_framework.core.logging_config import setup_logging

class Orchestrator:
    """
    The central hub for AetherML. Manages configuration, plugin loading,
    data pipeline setup, model initialization, training loops, and evaluation.
    Adheres to SRP by managing the training/evaluation lifecycle, not specific implementations.
    Adheres to DIP by depending on IModel, ICustomDataset, IDataPreprocessor, IAlgorithm abstractions.
    Adheres to OCP by allowing new plugins without modifying its core loop.
    """
    def __init__(self, config_path: str):
        setup_logging()
        logger.info(f"Orchestrator initializing with config from {config_path}")
        self.config: AetherMLConfig = self._load_config(config_path)
        
        self.device = torch.device(self.config.trainer.device)
        logger.info(f"Using device: {self.device}")

        self.plugin_manager = PluginManager(self.config.plugin_manager.plugin_dirs)
        self.plugin_manager.load_plugins()

        self.model: Optional[IModel] = None
        self.optimizer: Optional[torch.optim.Optimizer] = None
        self.loss_fn: Optional[nn.Module] = None
        self.algorithm: Optional[IAlgorithm] = None
        self.scheduler: Optional[Any] = None # Can be PyTorch LR scheduler or custom

        self.best_val_metric: float = float('inf') if self.config.trainer.save_best_model else -float('inf')
        self.best_metric_is_min: bool = True # Assume lower is better for loss
        self.current_epoch: int = 0
        self.epochs_no_improve: int = 0 # For early stopping

    def _load_config(self, config_path: str) -> AetherMLConfig:
        """Loads and validates configuration using Pydantic."""
        try:
            from yaml import safe_load # Defer import for cleaner core
            with open(config_path, 'r') as f:
                raw_config = safe_load(f)
            return AetherMLConfig(**raw_config)
        except Exception as e:
            logger.error(f"Error loading or validating config '{config_path}': {e}", exc_info=True)
            raise

    def _setup_data(self):
        """Sets up the dataset and data loaders."""
        logger.info("Setting up data pipeline...")
        dataset = self.plugin_manager.get_dataset(self.config.data)
        
        preprocessors = [self.plugin_manager.get_preprocessor(p_config) for p_config in self.config.data.preprocessors]
        data_pipeline = DataPipeline(preprocessors)

        # The dataset's __getitem__ will now return raw items,
        # and the collate_fn will apply the preprocessing pipeline.
        def collate_fn_with_pipeline(batch_list):
            processed_batch_list = [data_pipeline(item) for item in batch_list]
            # Convert list of dicts to dict of lists/tensors
            batch_dict = {key: [d[key] for d in processed_batch_list] for key in processed_batch_list[0]}
            # Stack tensors (assuming 'data' and 'label' are tensors)
            if 'data' in batch_dict and isinstance(batch_dict['data'][0], torch.Tensor):
                batch_dict['data'] = torch.stack(batch_dict['data'])
            if 'label' in batch_dict and isinstance(batch_dict['label'][0], torch.Tensor):
                batch_dict['label'] = torch.stack(batch_dict['label'])
            return batch_dict

        self.train_loader = DataLoader(
            dataset,
            batch_size=self.config.data.batch_size,
            shuffle=True,
            num_workers=self.config.data.num_workers,
            collate_fn=collate_fn_with_pipeline
        )
        # For validation/test, a simple split or another dataset would be needed.
        # For this example, we'll use a simplified approach or assume it's part of the dataset plugin logic.
        self.val_loader = DataLoader( # Using the same dataset for val for simplicity
            dataset,
            batch_size=self.config.data.batch_size,
            shuffle=False,
            num_workers=self.config.data.num_workers,
            collate_fn=collate_fn_with_pipeline
        )
        logger.info(f"Train/Validation loaders prepared with batch size: {self.config.data.batch_size}")

    def _setup_model(self):
        """Initializes the model, optimizer, loss function, and optionally scheduler."""
        logger.info("Setting up model, optimizer, and loss function...")
        self.model = self.plugin_manager.get_model(self.config.model).to(self.device)

        optimizer_cls = self.plugin_manager.get_optimizer_cls(self.config.optimizer.name)
        self.optimizer = optimizer_cls(self.model.parameters(), **self.config.optimizer.params)

        loss_fn_cls = self.plugin_manager.get_loss_fn_cls(self.config.loss_function.name)
        self.loss_fn = loss_fn_cls(**self.config.loss_function.params)

        if self.config.scheduler:
            scheduler_cls = self.plugin_manager.get_scheduler_cls(self.config.scheduler.name)
            self.scheduler = scheduler_cls(self.optimizer, **self.config.scheduler.params)
            logger.info(f"LR scheduler '{self.config.scheduler.name}' configured.")
        
        logger.info(f"Model: {self.model.__class__.__name__}")
        logger.info(f"Optimizer: {self.optimizer.__class__.__name__}")
        logger.info(f"Loss Function: {self.loss_fn.__class__.__name__}")

    def _setup_algorithm(self):
        """Initializes the chosen training/evaluation algorithm."""
        if not (self.model and self.loss_fn and self.optimizer):
            raise ValueError("Model, loss function, and optimizer must be set up before algorithm.")
        logger.info(f"Setting up algorithm: {self.config.algorithm.name}")
        self.algorithm = self.plugin_manager.get_algorithm(
            config=self.config.algorithm,
            model=self.model,
            loss_fn=self.loss_fn,
            optimizer=self.optimizer,
            device=self.device,
            scheduler=self.scheduler
        )

    def train(self):
        """Executes the main training and validation loop."""
        self.current_epoch = 0 # Reset epoch counter
        self.epochs_no_improve = 0 # Reset early stopping counter
        
        self._setup_data()
        self._setup_model()
        self._setup_algorithm()

        logger.info("Starting training loop...")
        for epoch in range(self.config.trainer.epochs):
            self.current_epoch = epoch
            logger.info(f"Epoch {epoch+1}/{self.config.trainer.epochs}")
            
            # Training phase
            self.model.train()
            total_train_metrics = {'loss': 0.0}
            start_time = time.time()
            for batch_idx, batch in enumerate(self.train_loader):
                metrics = self.algorithm.train_step(batch)
                for key, value in metrics.items():
                    total_train_metrics[key] = total_train_metrics.get(key, 0.0) + value
                if (batch_idx + 1) % self.config.trainer.log_interval_batches == 0:
                    logger.info(f"  Batch {batch_idx+1}/{len(self.train_loader)} - Train Metrics: {metrics}")
            
            avg_train_metrics = {key: value / len(self.train_loader) for key, value in total_train_metrics.items()}
            logger.info(f"Epoch {epoch+1} Training finished in {time.time() - start_time:.2f}s - Average Train Metrics: {avg_train_metrics}")

            # Validation phase
            self.model.eval()
            val_metrics = self.algorithm.evaluate_model(self.val_loader) # Use dedicated val_loader
            logger.info(f"Epoch {epoch+1} Validation Metrics: {val_metrics}")

            # Determine if current best metric should be minimized or maximized
            # For simplicity, assume 'loss' is always minimized. For other metrics (e.g., accuracy), this needs to be configured.
            if 'loss' in val_metrics:
                current_val_metric = val_metrics['loss']
            elif 'accuracy' in val_metrics: # Example for a metric to maximize
                current_val_metric = -val_metrics['accuracy'] # Invert for min-comparison
                self.best_metric_is_min = False
            else:
                logger.warning("No standard metric 'loss' or 'accuracy' found for best model tracking. Defaulting to 'loss'.")
                current_val_metric = float('inf')

            # Scheduler step (if configured)
            if self.scheduler:
                if self.config.scheduler.interval == "epoch":
                    if isinstance(self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
                        self.scheduler.step(current_val_metric) 
                    else:
                        self.scheduler.step()
                logger.info(f"Learning rate after scheduler step: {self.optimizer.param_groups[0]['lr']:.6f}")

            # Model saving and early stopping
            if self.config.trainer.save_best_model:
                if (current_val_metric < self.best_val_metric and self.best_metric_is_min) or \
                   (current_val_metric > self.best_val_metric and not self.best_metric_is_min):
                    self.best_val_metric = current_val_metric
                    os.makedirs(self.config.trainer.checkpoint_dir, exist_ok=True)
                    model_filename = f"best_model_{self.config.model.name}.pth"
                    model_path = os.path.join(self.config.trainer.checkpoint_dir, model_filename)
                    self.model.save(model_path)
                    logger.success(f"Best model saved to {model_path} with validation metric: {self.best_val_metric:.4f}")
                    self.epochs_no_improve = 0
                else:
                    self.epochs_no_improve += 1
                    logger.info(f"Validation metric did not improve for {self.epochs_no_improve} epochs.")
                    if self.config.trainer.early_stopping_patience and self.epochs_no_improve >= self.config.trainer.early_stopping_patience:
                        logger.warning(f"Early stopping triggered after {self.config.trainer.early_stopping_patience} epochs without improvement.")
                        break

        logger.info("Training complete.")

    def evaluate(self, dataloader: DataLoader) -> Dict[str, float]:
        """Evaluates the final model on a given dataloader."""
        if not self.model:
            logger.error("Model not trained or loaded. Cannot evaluate.")
            raise ValueError("Model not available for evaluation.")
        logger.info("Starting final evaluation...")
        self.model.eval()
        metrics = self.algorithm.evaluate_model(dataloader)
        logger.info(f"Final Evaluation Metrics: {metrics}")
        return metrics

```

---

### **AetherML Example Plugin Code (`aetherml_framework/plugins/example_plugin/`)**

GoldenDAG: `AETHER-GM-0012`
Trace ID: `T-1.0-PLUGIN_INIT-r1t2y3u4i5o6p7a8s9d0f1g2h3j4k5l6z7`
Codex ID: `C-PLUGIN-EXAMPLE_PLUGIN_INIT-v1.0-alpha`
```python
# aetherml_framework/plugins/example_plugin/__init__.py
# This file ensures Python recognizes example_plugin as a package.
```

GoldenDAG: `AETHER-GM-0013`
Trace ID: `T-1.0-SIMPLE_NN_MODEL-f1g2h3j4k5l6z7x8c9v0b1n2m3a4s5d6`
Codex ID: `C-PLUGIN-SIMPLE_NN_MODEL-v1.0-alpha`
```python
# aetherml_framework/plugins/example_plugin/model.py
import torch.nn as nn
import torch
from aetherml_framework.models.base_model import IModel
from typing import Dict, Any
from loguru import logger

class SimpleNN(IModel):
    """
    A simple Neural Network for classification or regression.
    Implements IModel interface.
    Adheres to SRP by defining only the network architecture and its forward pass.
    """
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, dropout_rate: float = 0.0):
        super().__init__()
        self.params = {'input_dim': input_dim, 'hidden_dim': hidden_dim, 'output_dim': output_dim, 'dropout_rate': dropout_rate}
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        logger.info(f"SimpleNN model initialized: {input_dim}->{hidden_dim}->{output_dim}")
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network."""
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

    def save(self, path: str):
        """Saves the model's state dictionary."""
        try:
            torch.save(self.state_dict(), path)
            logger.info(f"Model state saved to {path}")
        except Exception as e:
            logger.error(f"Failed to save model state to {path}: {e}", exc_info=True)

    def load(self, path: str):
        """Loads the model's state dictionary."""
        try:
            self.load_state_dict(torch.load(path, map_location=lambda storage, loc: storage)) # Map to CPU if needed
            logger.info(f"Model state loaded from {path}")
        except Exception as e:
            logger.error(f"Failed to load model state from {path}: {e}", exc_info=True)

```

GoldenDAG: `AETHER-GM-0014`
Trace ID: `T-1.0-SYNTHETIC_DATA-h1j2k3l4z5x6c7v8b9n0m1a2s3d4f5g6`
Codex ID: `C-PLUGIN-SYNTHETIC_DATA-v1.0-alpha`
```python
# aetherml_framework/plugins/example_plugin/data.py
import torch
from aetherml_framework.data.datasets import ICustomDataset
from aetherml_framework.data.pipeline import IDataPreprocessor
from typing import Any, Dict
from loguru import logger

class SyntheticDataset(ICustomDataset):
    """
    A simple dataset generating synthetic data for demonstration.
    Implements ICustomDataset interface.
    Adheres to SRP by focusing on raw data generation.
    """
    def load_data(self, num_samples: int = 1000, input_dim: int = 10, output_dim: int = 2):
        """Generates random data and labels."""
        self.data = [torch.randn(input_dim) for _ in range(num_samples)]
        self.labels = [torch.randint(0, output_dim, (1,)).squeeze(0) for _ in range(num_samples)]
        logger.info(f"Generated {num_samples} synthetic samples with input_dim={input_dim}, output_dim={output_dim}")

class NormalizePreprocessor(IDataPreprocessor):
    """
    A simple preprocessor to normalize data to [0, 1].
    Implements IDataPreprocessor interface.
    Adheres to SRP by focusing on a single data transformation.
    """
    def process(self, data_item: Dict[str, Any]) -> Dict[str, Any]:
        """Applies min-max normalization."""
        if 'data' in data_item and isinstance(data_item['data'], torch.Tensor):
            data_min = data_item['data'].min()
            data_max = data_item['data'].max()
            if data_max > data_min:
                data_item['data'] = (data_item['data'] - data_min) / (data_max - data_min)
            else: # Handle constant tensor case where min == max
                data_item['data'] = torch.zeros_like(data_item['data'])
        return data_item

```

GoldenDAG: `AETHER-GM-0015`
Trace ID: `T-1.0-STANDARD_TRAINING_ALG-c1v2b3n4m5l6k7j8h9g0f1d2s3a4`
Codex ID: `C-PLUGIN-STANDARD_TRAINING_ALG-v1.0-alpha`
```python
# aetherml_framework/plugins/example_plugin/algorithm.py
import torch
from aetherml_framework.algorithms.base_algorithm import IAlgorithm
from typing import Dict, Any
from loguru import logger

class StandardTrainingAlgorithm(IAlgorithm):
    """
    A standard training algorithm implementing common training, validation, and evaluation steps.
    Implements IAlgorithm interface.
    Adheres to SRP by focusing solely on the training/validation/evaluation logic.
    """
    def train_step(self, batch: Dict[str, Any]) -> Dict[str, float]:
        """
        Performs a single training step including forward pass, loss calculation,
        backward pass, and optimizer step.
        """
        self.model.train()
        self.optimizer.zero_grad()

        data = batch['data'].to(self.device)
        labels = batch['label'].to(self.device)

        outputs = self.model(data)
        loss = self.loss_fn(outputs, labels)
        
        loss.backward()
        self.optimizer.step()

        # Assuming classification for accuracy, can be extended for other metrics
        _, predicted = torch.max(outputs.data, 1)
        accuracy = (predicted == labels).sum().item() / labels.size(0)

        return {'loss': loss.item(), 'accuracy': accuracy}

    def validate_step(self, batch: Dict[str, Any]) -> Dict[str, float]:
        """
        Performs a single validation step (no gradient updates).
        """
        self.model.eval()
        with torch.no_grad():
            data = batch['data'].to(self.device)
            labels = batch['label'].to(self.device)

            outputs = self.model(data)
            loss = self.loss_fn(outputs, labels)

            _, predicted = torch.max(outputs.data, 1)
            accuracy = (predicted == labels).sum().item() / labels.size(0)

        return {'loss': loss.item(), 'accuracy': accuracy}

    def evaluate_model(self, dataloader: torch.utils.data.DataLoader) -> Dict[str, float]:
        """
        Evaluates the model on an entire dataloader.
        """
        self.model.eval()
        total_loss = 0
        total_correct = 0
        total_samples = 0
        with torch.no_grad():
            for batch in dataloader:
                data = batch['data'].to(self.device)
                labels = batch['label'].to(self.device)

                outputs = self.model(data)
                loss = self.loss_fn(outputs, labels)
                total_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total_correct += (predicted == labels).sum().item()
                total_samples += labels.size(0)
        
        avg_loss = total_loss / len(dataloader)
        accuracy = total_correct / total_samples
        return {'loss': avg_loss, 'accuracy': accuracy}

```

---

### **Example Configuration (`config.yaml`)**

GoldenDAG: `AETHER-GM-0016`
Trace ID: `T-1.0-CONFIG_FILE-g1h2j3k4l5z6x7c8v9b0n1m2a3s4d5`
Codex ID: `C-CONFIG-EXAMPLE_CONFIG-v1.0-alpha`
```yaml
# config.yaml
# This file defines the operational blueprint for an AetherML run,
# leveraging Pydantic for validation and plugin names for dynamic loading.

plugin_manager:
  plugin_dirs: ["aetherml_framework/plugins"] # Scans this directory for plugins

model:
  name: "SimpleNN" # Refers to SimpleNN class in plugins/example_plugin/model.py
  params:
    input_dim: 10
    hidden_dim: 64
    output_dim: 2

data:
  dataset_name: "SyntheticDataset" # Refers to SyntheticDataset in plugins/example_plugin/data.py
  dataset_params:
    num_samples: 1000
    input_dim: 10
    output_dim: 2
  batch_size: 64
  num_workers: 0
  preprocessors:
    - name: "NormalizePreprocessor" # Refers to NormalizePreprocessor in plugins/example_plugin/data.py
      params: {} # No params for this specific preprocessor

optimizer:
  name: "Adam" # PyTorch's Adam optimizer
  params:
    lr: 0.001

# Optional: Uncomment and configure for learning rate scheduling
# scheduler:
#   name: "StepLR"
#   params:
#     step_size: 5
#     gamma: 0.1
#   interval: "epoch" # Can be "epoch" or "step"

loss_function:
  name: "CrossEntropyLoss" # PyTorch's CrossEntropyLoss
  params: {}

trainer:
  device: "cuda" # or "cpu" - automatically defaults to cuda if available
  epochs: 10
  log_interval_batches: 10
  save_best_model: True
  checkpoint_dir: "aetherml_checkpoints" # Directory to save the best model
  early_stopping_patience: 3 # Stop if validation loss doesn't improve for 3 epochs

algorithm:
  name: "StandardTrainingAlgorithm" # Refers to StandardTrainingAlgorithm in plugins/example_plugin/algorithm.py
  params: {} # No specific params for this algorithm beyond base init
```

---

### **Example Usage / Entry Point (`main.py`)**

GoldenDAG: `AETHER-GM-0017`
Trace ID: `T-1.0-MAIN_ENTRYPOINT-p1o2i3u4y5t6r7e8w9q0a1s2d3f4g5`
Codex ID: `C-CORE-APPLICATION_LOGIC-MAIN_ENTRYPOINT-v1.0-alpha`
```python
# aetherml_framework/main.py
import os
from aetherml_framework.core.orchestrator import Orchestrator
from loguru import logger

# Ensure the plugins directory exists for the example setup
PLUGINS_DIR = "aetherml_framework/plugins"
if not os.path.exists(PLUGINS_DIR):
    os.makedirs(PLUGINS_DIR)
    # Create an empty __init__.py if it doesn't exist to make it a package
    with open(os.path.join(PLUGINS_DIR, '__init__.py'), 'w') as f:
        pass
    # Also create the example_plugin directory structure if needed
    example_plugin_path = os.path.join(PLUGINS_DIR, "example_plugin")
    if not os.path.exists(example_plugin_path):
        os.makedirs(example_plugin_path)
        with open(os.path.join(example_plugin_path, '__init__.py'), 'w') as f:
            pass
logger.info(f"Ensured plugin directory structure exists at {PLUGINS_DIR}")


# Create a sample config file for demonstration if it doesn't exist
CONFIG_FILE_PATH = "config.yaml"
if not os.path.exists(CONFIG_FILE_PATH):
    example_config_content = """
plugin_manager:
  plugin_dirs: ["aetherml_framework/plugins"]

model:
  name: "SimpleNN"
  params:
    input_dim: 10
    hidden_dim: 64
    output_dim: 2

data:
  dataset_name: "SyntheticDataset"
  dataset_params:
    num_samples: 1000
    input_dim: 10
    output_dim: 2
  batch_size: 64
  num_workers: 0
  preprocessors:
    - name: "NormalizePreprocessor"
      params: {}

optimizer:
  name: "Adam"
  params:
    lr: 0.001

loss_function:
  name: "CrossEntropyLoss"
  params: {}

trainer:
  device: "cuda" # or "cpu"
  epochs: 10
  log_interval_batches: 10
  save_best_model: True
  checkpoint_dir: "aetherml_checkpoints"
  early_stopping_patience: 3

algorithm:
  name: "StandardTrainingAlgorithm"
  params: {}
"""
    with open(CONFIG_FILE_PATH, 'w') as f:
        f.write(example_config_content)
    logger.info(f"Generated default '{CONFIG_FILE_PATH}' for demonstration.")

def main():
    """Main entry point to run the AetherML framework."""
    logger.info("AetherML Framework starting...")
    try:
        orchestrator = Orchestrator(config_path=CONFIG_FILE_PATH)
        orchestrator.train()
        
        # Optionally load the best model and evaluate again
        if orchestrator.config.trainer.save_best_model and orchestrator.model:
            logger.info("Loading best model for final evaluation...")
            best_model_path = os.path.join(orchestrator.config.trainer.checkpoint_dir, f"best_model_{orchestrator.config.model.name}.pth")
            if os.path.exists(best_model_path):
                # We need to re-instantiate the model class to ensure it's a fresh state
                final_model = orchestrator.plugin_manager.get_model(orchestrator.config.model).to(orchestrator.device)
                final_model.load(best_model_path)
                orchestrator.model = final_model # Update orchestrator's model for evaluation
                
                # Evaluate on the validation loader, as it's typically used for final metrics
                final_eval_metrics = orchestrator.evaluate(orchestrator.val_loader) 
                logger.success(f"Final model evaluation metrics (on validation set): {final_eval_metrics}")
            else:
                logger.warning(f"Best model not found at {best_model_path}. Skipping final evaluation.")

    except Exception as e:
        logger.error(f"An unhandled error occurred during AetherML execution: {e}", exc_info=True)
    finally:
        logger.info("AetherML Framework finished.")

if __name__ == "__main__":
    # This block executes when the script is run directly
    # Ensure plugins are available in sys.path if not running as a package
    # For this example, assuming current working directory is 'aetherml_framework' parent
    # or that 'aetherml_framework' is a Python package installed or available in PYTHONPATH.
    # The plugin_manager is designed to find plugins relative to 'aetherml_framework/plugins'
    # so simple execution from the project root (where main.py resides) should work.
    main()

```
