"""
Summarization using transformers
"""

from typing import Optional, List



class Summarizer:
    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        device: Optional[str] = None
    ):
        """
        Initialize summarizer.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load summarization pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "summarization",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def summarize(
        self,
        text: str,
        max_length: int = 130,
        min_length: int = 30,
        **kwargs
    ) -> str:
        """
        Summarize text.
        
        Args:
            text: Text to summarize.
            max_length: Maximum summary length.
            min_length: Minimum summary length.
            
        Returns:
            Summary text.
        """
        pipeline = self._get_pipeline()
        
        result = pipeline(
            text,
            max_length=max_length,
            min_length=min_length,
            **kwargs
        )
        
        return result[0]["summary_text"]
    
    def summarize_batch(
        self,
        texts: List[str],
        **kwargs
    ) -> List[str]:
        """
        Summarize multiple texts.
        
        Args:
            texts: List of texts to summarize.
            
        Returns:
            List of summaries.
        """
        pipeline = self._get_pipeline()
        
        results = pipeline(texts, **kwargs)
        return [r["summary_text"] for r in results]


def quick_summarize(text: str, max_length: int = 130) -> str:
    """
    Quick summarization.
    
    Args:
        text: Text to summarize.
        max_length: Maximum summary length.
        
    Returns:
        Summary.
    """
    summarizer = Summarizer()
    return summarizer.summarize(text, max_length=max_length)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.summarize <text>")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    
    summary = quick_summarize(text)
    print(f"Summary:\n{summary}")
