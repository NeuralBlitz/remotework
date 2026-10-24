"""
AI Utilities - EasyOCR wrapper for text recognition
"""

from pathlib import Path
from typing import Optional, List, Dict
import numpy as np


class OCREngine:
    def __init__(self, languages: Optional[List[str]] = None, use_gpu: bool = False):
        """
        Initialize OCR engine.
        
        Args:
            languages: List of language codes (e.g., ['en', 'ch_sim']). 
                      Defaults to ['en'].
            use_gpu: Whether to use GPU acceleration.
        """
        self.languages = languages or ['en']
        self.use_gpu = use_gpu
        self.reader = None
    
    def _get_reader(self):
        """Lazy load the OCR reader."""
        if self.reader is None:
            try:
                import easyocr
                self.reader = easyocr.Reader(
                    self.languages, 
                    gpu=self.use_gpu,
                    verbose=False
                )
            except ImportError:
                raise ImportError(
                    "easyocr not installed. Install with: pip install easyocr"
                )
        return self.reader
    
    def read_text(self, image_path: str) -> List[Dict]:
        """
        Read text from an image file.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            List of dictionaries with 'text', 'confidence', and bounding box.
        """
        reader = self._get_reader()
        results = reader.readtext(image_path)
        
        return [
            {
                'text': text,
                'confidence': conf,
                'bbox': box
            }
            for box, text, conf in results
        ]
    
    def read_text_from_array(self, image_array) -> List[Dict]:
        """
        Read text from a numpy array (image).
        
        Args:
            image_array: NumPy array representing the image.
            
        Returns:
            List of dictionaries with 'text', 'confidence', and bounding box.
        """
        reader = self._get_reader()
        results = reader.readtext(image_array)
        
        return [
            {
                'text': text,
                'confidence': conf,
                'bbox': box
            }
            for box, text, conf in results
        ]
    
    def extract_text_only(self, image_path: str) -> str:
        """
        Extract plain text from an image.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Extracted text as a string.
        """
        results = self.read_text(image_path)
        return ' '.join(r['text'] for r in results)


def quick_ocr(image_path: str, languages: Optional[List[str]] = None) -> str:
    """
    Quick OCR function for simple use cases.
    
    Args:
        image_path: Path to the image file.
        languages: Optional list of language codes.
        
    Returns:
        Extracted text.
    """
    engine = OCREngine(languages=languages)
    return engine.extract_text_only(image_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.ocr <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print(f"Processing: {image_path}")
    text = quick_ocr(image_path)
    print(f"\nExtracted text:\n{text}")
