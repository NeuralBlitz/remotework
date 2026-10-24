"""
AI Utilities - Text generation with transformers
"""

from typing import Optional, List, Dict, Any
import os


class TextGenerator:
    def __init__(
        self, 
        model_name: str = "gpt2",
        device: Optional[str] = None
    ):
        """
        Initialize text generation model.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use ('cuda', 'cpu', or None for auto).
        """
        self.model_name = model_name
        self.device = device or ('cuda' if os.environ.get('CUDA_VISIBLE_DEVICES') else 'cpu')
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load the generation pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device=-1 if self.device == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with: pip install transformers"
                )
        return self.pipeline
    
    def generate(
        self,
        prompt: str,
        max_length: int = 100,
        num_return_sequences: int = 1,
        temperature: float = 0.9,
        top_p: float = 0.9,
        do_sample: bool = True,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input text prompt.
            max_length: Maximum length of generated text.
            num_return_sequences: Number of sequences to generate.
            temperature: Sampling temperature (lower = more deterministic).
            top_p: Nucleus sampling threshold.
            do_sample: Whether to use sampling.
            
        Returns:
            List of dictionaries with 'generated_text'.
        """
        pipeline = self._get_pipeline()
        
        results = pipeline(
            prompt,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            **kwargs
        )
        
        return results
    
    def generate_single(
        self,
        prompt: str,
        max_length: int = 100,
        **kwargs
    ) -> str:
        """
        Generate a single text response.
        
        Args:
            prompt: Input text prompt.
            max_length: Maximum length of generated text.
            
        Returns:
            Generated text string.
        """
        results = self.generate(prompt, max_length=max_length, num_return_sequences=1, **kwargs)
        return results[0]['generated_text']


def quick_generate(
    prompt: str,
    model_name: str = "gpt2",
    max_length: int = 100
) -> str:
    """
    Quick text generation function.
    
    Args:
        prompt: Input text prompt.
        model_name: HuggingFace model name.
        max_length: Maximum length of generated text.
        
    Returns:
        Generated text.
    """
    generator = TextGenerator(model_name=model_name)
    return generator.generate_single(prompt, max_length=max_length)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        prompt = "Once upon a time"
    else:
        prompt = ' '.join(sys.argv[1:])
    
    print(f"Prompt: {prompt}\n")
    result = quick_generate(prompt)
    print(f"Generated:\n{result}")
