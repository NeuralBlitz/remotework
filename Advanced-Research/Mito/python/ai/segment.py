"""
Image Segmentation using transformers
"""

from typing import List, Dict, Any, Optional



class Segmenter:
    def __init__(
        self,
        model_name: str = "facebook/maskformer-swin-base-ade",
        device: Optional[str] = None
    ):
        """
        Initialize segmenter.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "image-segmentation",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError("transformers not installed")
        return self.pipeline
    
    def segment(self, image_path: str, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Segment image into parts."""
        pipeline = self._get_pipeline()
        results = pipeline(image_path)
        return [r for r in results if r.get("score", 1.0) >= threshold]


def quick_segment(image_path: str) -> List[Dict]:
    """Quick segmentation."""
    return Segmenter().segment(image_path)


if __name__ == '__main__':
    import sys
    results = quick_segment(sys.argv[1] if len(sys.argv) > 1 else "image.jpg")
    for r in results:
        print(f"{r['label']}: {r['score']:.2f}")
