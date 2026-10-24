"""
LLama.cpp Python bindings wrapper
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import os


class LlamaModel:
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 512,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        verbose: bool = False
    ):
        """
        Initialize Llama model.
        
        Args:
            model_path: Path to GGUF model file.
            n_ctx: Context size.
            n_threads: CPU threads to use.
            n_gpu_layers: Number of layers to offload to GPU.
            verbose: Enable verbose output.
        """
        self.model_path = Path(model_path)
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose
        self.llama = None
        self.model = None
        
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
    
    def _get_llama(self):
        """Lazy load llama-cpp-python."""
        if self.llama is None:
            try:
                from llama_cpp import Llama
                self.llama = Llama
            except ImportError:
                raise ImportError(
                    "llama-cpp-python not installed. Install with:\n"
                    "  pip install llama-cpp-python\n"
                    "  # or with GPU support:\n"
                    "  pip install llama-cpp-python[cublas]"
                )
        return self.llama
    
    def load(self):
        """Load the model into memory."""
        Llama = self._get_llama()
        
        if self.verbose:
            print(f"Loading model from {self.model_path}...")
        
        self.model = Llama(
            model_path=str(self.model_path),
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=self.verbose
        )
        
        if self.verbose:
            print("Model loaded successfully!")
        
        return self
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 128,
        temperature: float = 0.7,
        top_p: float = 0.95,
        top_k: int = 40,
        repeat_penalty: float = 1.1,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], None]:
        """
        Generate text from prompt.
        
        Args:
            prompt: Input prompt.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling.
            top_k: Top-k sampling.
            repeat_penalty: Repetition penalty.
            stream: Stream output token by token.
            
        Returns:
            Generated text dict or None if streaming.
        """
        if self.model is None:
            self.load()
        
        if stream:
            return self._stream_generate(
                prompt, max_tokens, temperature, top_p, top_k, repeat_penalty
            )
        
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repeat_penalty=repeat_penalty,
            **kwargs
        )
        
        return output
    
    def _stream_generate(self, prompt, max_tokens, temperature, top_p, top_k, repeat_penalty):
        """Stream generation token by token."""
        if self.model is None:
            self.load()
        
        for token in self.model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            repeat_penalty=repeat_penalty,
            stream=True
        ):
            yield token
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat completion style generation.
        
        Args:
            messages: List of message dicts with 'role' and 'content'.
            
        Returns:
            Response dict.
        """
        if self.model is None:
            self.load()
        
        try:
            from llama_cpp import ChatCompletion
            
            output = ChatCompletion.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return output
        except Exception:
            prompt = self._messages_to_prompt(messages)
            return self.generate(prompt, **kwargs)
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert chat messages to prompt."""
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg["content"]
            
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant:"
        return prompt
    
    def __enter__(self):
        """Context manager entry."""
        self.load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.model = None


def load_model(
    model_path: str,
    n_ctx: int = 512,
    n_threads: int = 4,
    **kwargs
) -> LlamaModel:
    """
    Quick function to load a model.
    
    Args:
        model_path: Path to GGUF model.
        n_ctx: Context size.
        n_threads: CPU threads.
        
    Returns:
        Loaded LlamaModel instance.
    """
    return LlamaModel(model_path, n_ctx, n_threads, **kwargs).load()


def quick_generate(
    prompt: str,
    model_path: str = "model.gguf",
    max_tokens: int = 128,
    **kwargs
) -> str:
    """
    Quick text generation.
    
    Args:
        prompt: Input prompt.
        model_path: Path to model.
        max_tokens: Max tokens to generate.
        
    Returns:
        Generated text.
    """
    model = LlamaModel(model_path, verbose=False)
    result = model.generate(prompt, max_tokens=max_tokens, **kwargs)
    return result["choices"][0]["text"]


if __name__ == '__main__':
    import sys
    
    model_path = sys.argv[1] if len(sys.argv) > 1 else "model.gguf"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Hello, how are you?"
    
    print(f"Model: {model_path}")
    print(f"Prompt: {prompt}\n")
    
    try:
        result = quick_generate(prompt, model_path)
        print(f"Response:\n{result}")
    except FileNotFoundError:
        print(f"Error: Model file '{model_path}' not found.")
        print("Download a GGUF model and place it in the project directory.")
    except ImportError as e:
        print(f"Error: {e}")
