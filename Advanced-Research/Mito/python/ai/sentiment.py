"""
Sentiment Analysis using transformers
"""

from typing import Optional, List, Dict, Any


class SentimentAnalyzer:
    def __init__(
        self,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        device: Optional[str] = None
    ):
        """
        Initialize sentiment analyzer.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load the sentiment pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "sentiment-analysis",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Input text.
            
        Returns:
            Dict with 'label' and 'score'.
        """
        pipeline = self._get_pipeline()
        result = pipeline(text)[0]
        return result
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment of multiple texts.
        
        Args:
            texts: List of input texts.
            
        Returns:
            List of results.
        """
        pipeline = self._get_pipeline()
        return pipeline(texts)
    
    def get_sentiment(self, text: str) -> str:
        """
        Get simple sentiment label.
        
        Args:
            text: Input text.
            
        Returns:
            'POSITIVE' or 'NEGATIVE'.
        """
        result = self.analyze(text)
        return result['label']
    
    def get_score(self, text: str) -> float:
        """
        Get sentiment confidence score.
        
        Args:
            text: Input text.
            
        Returns:
            Confidence score between 0 and 1.
        """
        result = self.analyze(text)
        return result['score']


class EmotionDetector:
    def __init__(self):
        """Initialize emotion detector."""
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load the emotion detection pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    top_k=None
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect emotions in text.
        
        Args:
            text: Input text.
            
        Returns:
            List of emotions with scores.
        """
        pipeline = self._get_pipeline()
        result = pipeline(text)[0]
        return sorted(result, key=lambda x: x['score'], reverse=True)
    
    def get_dominant(self, text: str) -> str:
        """
        Get dominant emotion.
        
        Args:
            text: Input text.
            
        Returns:
            Dominant emotion label.
        """
        emotions = self.detect(text)
        return emotions[0]['label']


def quick_sentiment(text: str) -> Dict[str, Any]:
    """
    Quick sentiment analysis.
    
    Args:
        text: Input text.
        
    Returns:
        Sentiment result.
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


def quick_emotion(text: str) -> str:
    """
    Quick emotion detection.
    
    Args:
        text: Input text.
        
    Returns:
        Dominant emotion.
    """
    detector = EmotionDetector()
    return detector.get_dominant(text)


if __name__ == '__main__':
    import sys
    
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "I love this product!"
    
    print(f"Text: {text}\n")
    
    result = quick_sentiment(text)
    print(f"Sentiment: {result['label']} (score: {result['score']:.4f})")
    
    emotion = quick_emotion(text)
    print(f"Emotion: {emotion}")
