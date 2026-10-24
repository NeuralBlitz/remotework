"""
Model Management for Mito
Download, cache, and manage AI models
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
import time


class ModelType(Enum):
    LLAMA = "llama"
    TRANSFORMER = "transformer"
    WHISPER = "whisper"
    TTS = "tts"
    CUSTOM = "custom"


class ModelStatus(Enum):
    DOWNLOADING = "downloading"
    READY = "ready"
    ERROR = "error"
    LOADING = "loading"


@dataclass
class ModelInfo:
    name: str
    model_type: ModelType
    path: str
    size: int
    status: ModelStatus = ModelStatus.READY
    hash: Optional[str] = None
    downloaded_at: Optional[float] = None
    metadata: Dict = field(default_factory=dict)


class ModelManager:
    def __init__(self, models_dir: str = "./models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, ModelInfo] = {}
        self.registry_path = self.models_dir / ".registry.json"
        self._load_registry()
    
    def _load_registry(self):
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                for name, info in data.items():
                    self.models[name] = ModelInfo(
                        name=info["name"],
                        model_type=ModelType(info["model_type"]),
                        path=info["path"],
                        size=info["size"],
                        status=ModelStatus(info.get("status", "ready")),
                        hash=info.get("hash"),
                        downloaded_at=info.get("downloaded_at"),
                        metadata=info.get("metadata", {})
                    )
    
    def _save_registry(self):
        data = {
            name: {
                "name": info.name,
                "model_type": info.model_type.value,
                "path": info.path,
                "size": info.size,
                "status": info.status.value,
                "hash": info.hash,
                "downloaded_at": info.downloaded_at,
                "metadata": info.metadata
            }
            for name, info in self.models.items()
        }
        
        with open(self.registry_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register(self, name: str, path: str, model_type: ModelType = ModelType.CUSTOM, metadata: Dict = None) -> ModelInfo:
        """Register an existing model"""
        full_path = Path(path)
        size = full_path.stat().st_size if full_path.exists() else 0
        
        info = ModelInfo(
            name=name,
            model_type=model_type,
            path=str(full_path),
            size=size,
            status=ModelStatus.READY,
            downloaded_at=time.time(),
            metadata=metadata or {}
        )
        
        self.models[name] = info
        self._save_registry()
        
        return info
    
    def download(
        self,
        name: str,
        url: str,
        model_type: ModelType = ModelType.CUSTOM,
        progress_callback: Optional[Callable] = None
    ) -> ModelInfo:
        """Download a model from URL"""
        import urllib.request
        
        self.models[name] = ModelInfo(
            name=name,
            model_type=model_type,
            path="",
            size=0,
            status=ModelStatus.DOWNLOADING
        )
        
        dest_path = self.models_dir / f"{name}.gguf"
        
        def reporthook(block_num, block_size, total_size):
            if progress_callback:
                downloaded = block_num * block_size
                progress_callback(downloaded, total_size)
        
        urllib.request.urlretrieve(url, dest_path, reporthook)
        
        size = dest_path.stat().st_size
        
        info = ModelInfo(
            name=name,
            model_type=model_type,
            path=str(dest_path),
            size=size,
            status=ModelStatus.READY,
            downloaded_at=time.time()
        )
        
        self.models[name] = info
        self._save_registry()
        
        return info
    
    def load(self, name: str) -> any:
        """Load a model into memory"""
        if name not in self.models:
            raise ValueError(f"Model '{name}' not found")
        
        info = self.models[name]
        info.status = ModelStatus.LOADING
        
        # For GGUF models
        if info.model_type == ModelType.LLAMA:
            from python.ai.llama import LlamaModel
            model = LlamaModel(info.path)
            model.load()
            return model
        
        return None
    
    def get(self, name: str) -> Optional[ModelInfo]:
        """Get model info"""
        return self.models.get(name)
    
    def list(self, model_type: Optional[ModelType] = None) -> List[ModelInfo]:
        """List all models"""
        if model_type:
            return [m for m in self.models.values() if m.model_type == model_type]
        return list(self.models.values())
    
    def delete(self, name: str):
        """Delete a model"""
        if name in self.models:
            info = self.models[name]
            if Path(info.path).exists():
                Path(info.path).unlink()
            del self.models[name]
            self._save_registry()
    
    def get_size(self, name: str) -> int:
        """Get model size in bytes"""
        if name in self.models:
            return self.models[name].size
        return 0
    
    def get_total_size(self) -> int:
        """Get total size of all models"""
        return sum(m.size for m in self.models.values())
    
    def clear_cache(self):
        """Clear all cached models"""
        for name in list(self.models.keys()):
            self.delete(name)


class HuggingFaceHub:
    """Download models from HuggingFace"""
    
    BASE_URL = "https://huggingface.co"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
    
    def get_model_info(self, model_id: str) -> Dict:
        """Get model info from HuggingFace"""
        import requests
        
        url = f"{self.BASE_URL}/api/models/{model_id}"
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def download_file(
        self,
        model_id: str,
        filename: str,
        dest_path: str,
        progress: bool = True
    ):
        """Download a file from HuggingFace"""
        import requests
        
        url = f"{self.BASE_URL}/{model_id}/resolve/main/{filename}"
        
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        total = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress:
                        print(f"\rDownloaded: {downloaded}/{total} bytes", end="")
        
        if progress:
            print()
    
    def search_models(self, query: str, limit: int = 10) -> List[Dict]:
        """Search models on HuggingFace"""
        import requests
        
        url = f"{self.BASE_URL}/api/models"
        params = {"search": query, "limit": limit}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()


class ModelCache:
    """LRU cache for loaded models"""
    
    def __init__(self, max_size: int = 3):
        self.max_size = max_size
        self.cache: Dict[str, any] = {}
        self.access_order: List[str] = []
    
    def get(self, name: str) -> Optional[any]:
        if name in self.cache:
            self.access_order.remove(name)
            self.access_order.append(name)
            return self.cache[name]
        return None
    
    def put(self, name: str, model: any):
        if name in self.cache:
            self.access_order.remove(name)
        elif len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        self.cache[name] = model
        self.access_order.append(name)
    
    def clear(self):
        self.cache.clear()
        self.access_order.clear()


# Quick functions
def list_models() -> List[str]:
    """List available models"""
    manager = ModelManager()
    return [m.name for m in manager.list()]


def get_model(name: str) -> Optional[ModelInfo]:
    """Get model info"""
    manager = ModelManager()
    return manager.get(name)


def download_model(name: str, url: str):
    """Download a model"""
    manager = ModelManager()
    return manager.download(name, url)


if __name__ == '__main__':
    manager = ModelManager()
    
    print("Available models:")
    for m in manager.list():
        print(f"  - {m.name} ({m.model_type.value})")
