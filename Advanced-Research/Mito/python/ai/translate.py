"""
Translation using transformers
"""

from typing import Optional, List, Dict, Any



class Translator:
    def __init__(
        self,
        model_name: str = "Helsinki-NLP/opus-mt-en-es",
        device: Optional[str] = None
    ):
        """
        Initialize translator.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load translation pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "translation",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def translate(self, text: str, **kwargs) -> str:
        """
        Translate text.
        
        Args:
            text: Text to translate.
            
        Returns:
            Translated text.
        """
        pipeline = self._get_pipeline()
        result = pipeline(text, **kwargs)
        return result[0]["translation_text"]
    
    def translate_batch(self, texts: List[str], **kwargs) -> List[str]:
        """
        Translate multiple texts.
        
        Args:
            texts: List of texts to translate.
            
        Returns:
            List of translated texts.
        """
        pipeline = self._get_pipeline()
        results = pipeline(texts, **kwargs)
        return [r["translation_text"] for r in results]


def quick_translate(text: str, model: str = "Helsinki-NLP/opus-mt-en-es") -> str:
    """
    Quick translation.
    
    Args:
        text: Text to translate.
        model: Model name.
        
    Returns:
        Translated text.
    """
    translator = Translator(model_name=model)
    return translator.translate(text)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.translate <text>")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    result = quick_translate(text)
    print(f"Translation: {result}")
