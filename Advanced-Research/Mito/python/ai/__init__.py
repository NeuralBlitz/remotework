"""
AI Utilities Package

A collection of AI/ML utilities for:
- OCR text recognition
- Text generation
- Image classification
- Sentiment analysis
- Speech recognition
- Translation
- Embeddings
- Summarization
- Question answering
- Text-to-speech
"""

from .ocr import OCREngine, quick_ocr
from .textgen import TextGenerator, quick_generate
from .llama import LlamaModel, load_model, quick_generate as quick_llama
from .image_classify import ImageClassifier, quick_classify
from .sentiment import SentimentAnalyzer, EmotionDetector, quick_sentiment, quick_emotion
from .speech import SpeechRecognizer, quick_transcribe
from .translate import Translator, quick_translate
from .embeddings import Embedder, quick_embed
from .summarize import Summarizer, quick_summarize
from .qa import QAModel, quick_qa
from .tts import TTSEngine, quick_speak

__version__ = "1.0.0"
__all__ = [
    # OCR
    "OCREngine",
    "quick_ocr",
    # Text Generation
    "TextGenerator",
    "quick_generate",
    # Llama
    "LlamaModel",
    "load_model",
    "quick_llama",
    # Image Classification
    "ImageClassifier",
    "quick_classify",
    # Sentiment
    "SentimentAnalyzer",
    "EmotionDetector",
    "quick_sentiment",
    "quick_emotion",
    # Speech
    "SpeechRecognizer",
    "quick_transcribe",
    # Translation
    "Translator",
    "quick_translate",
    # Embeddings
    "Embedder",
    "quick_embed",
    # Summarization
    "Summarizer",
    "quick_summarize",
    # QA
    "QAModel",
    "quick_qa",
    # TTS
    "TTSEngine",
    "quick_speak",
]
