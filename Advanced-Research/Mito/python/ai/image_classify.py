"""
Image Classification using transformers
"""

from typing import Optional, List, Dict, Any
from pathlib import Path


class ImageClassifier:
    def __init__(
        self,
        model_name: str = "google/vit-base-patch16-224",
        device: Optional[str] = None
    ):
        """
        Initialize image classifier.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use ('cuda', 'cpu').
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
        self.classifier = None
        self.torch = None
    
    def _get_pipeline(self):
        """Lazy load the classification pipeline."""
        if self.pipeline is None:
            try:
                from transformers import AutoImageProcessor, AutoModelForImageClassification
                import torch
                self.torch = torch
                from PIL import Image
                
                self.Image = Image
                
                if self.device is None:
                    self.device = "cuda" if torch.cuda.is_available() else "cpu"
                
                self.processor = AutoImageProcessor.from_pretrained(self.model_name)
                self.classifier = AutoModelForImageClassification.from_pretrained(
                    self.model_name
                )
                self.classifier.to(self.device)
                self.classifier.eval()
                
            except ImportError as e:
                raise ImportError(
                    f"Missing dependencies: {e}\n"
                    "Install with: pip install transformers torch pillow"
                )
        return self
    
    def classify(
        self,
        image_path: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Classify an image.
        
        Args:
            image_path: Path to image file.
            top_k: Number of top predictions to return.
            
        Returns:
            List of dicts with 'label' and 'score'.
        """
        self._get_pipeline()
        
        image = self.Image.open(image_path)
        
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with self.torch.no_grad():
            outputs = self.classifier(**inputs)
        
        probs = outputs.logits.softmax(dim=-1)
        top_probs, top_indices = probs.topk(top_k)
        
        results = []
        for prob, idx in zip(top_probs[0], top_indices[0]):
            results.append({
                'score': prob.item(),
                'label': self.classifier.config.id2label[idx.item()]
            })
        
        return results
    
    def classify_url(self, url: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Classify an image from URL.
        
        Args:
            url: Image URL.
            top_k: Number of top predictions.
            
        Returns:
            List of predictions.
        """
        self._get_pipeline()
        
        import requests
        from io import BytesIO
        
        response = requests.get(url)
        image = self.Image.open(BytesIO(response.content))
        
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with self.torch.no_grad():
            outputs = self.classifier(**inputs)
        
        probs = outputs.logits.softmax(dim=-1)
        top_probs, top_indices = probs.topk(top_k)
        
        results = []
        for prob, idx in zip(top_probs[0], top_indices[0]):
            results.append({
                'score': prob.item(),
                'label': self.classifier.config.id2label[idx.item()]
            })
        
        return results


def quick_classify(image_path: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Quick image classification.
    
    Args:
        image_path: Path to image.
        top_k: Number of predictions.
        
    Returns:
        List of predictions.
    """
    classifier = ImageClassifier()
    return classifier.classify(image_path, top_k=top_k)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.image_classify <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print(f"Classifying: {image_path}\n")
    
    results = quick_classify(image_path)
    
    print("Predictions:")
    for r in results:
        print(f"  {r['label']}: {r['score']:.4f}")
