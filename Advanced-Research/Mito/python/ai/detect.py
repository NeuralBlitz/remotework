"""
Object Detection using transformers
"""

from typing import List, Dict, Any, Optional
from pathlib import Path



class ObjectDetector:
    def __init__(
        self,
        model_name: str = "facebook/detr-resnet-50",
        device: Optional[str] = None
    ):
        """
        Initialize object detector.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load detection pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "object-detection",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def detect(self, image_path: str, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Detect objects in image.
        
        Args:
            image_path: Path to image.
            threshold: Confidence threshold.
            
        Returns:
            List of detected objects with bbox, label, score.
        """
        pipeline = self._get_pipeline()
        
        results = pipeline(image_path)
        
        filtered = [r for r in results if r["score"] >= threshold]
        
        return filtered
    
    def detect_batch(self, image_paths: List[str], threshold: float = 0.5) -> List[List[Dict]]:
        """Detect objects in multiple images."""
        pipeline = self._get_pipeline()
        
        results = pipeline(image_paths)
        
        return [[r for r in res if r["score"] >= threshold] for res in results]


def quick_detect(image_path: str, threshold: float = 0.5) -> List[Dict[str, Any]]:
    """Quick object detection."""
    detector = ObjectDetector()
    return detector.detect(image_path, threshold)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.detect <image>")
        sys.exit(1)
    
    results = quick_detect(sys.argv[1])
    for r in results:
        print(f"{r['label']}: {r['score']:.2f}")
