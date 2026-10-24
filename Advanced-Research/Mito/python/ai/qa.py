"""
Question Answering using transformers
"""

from typing import Optional, Dict, Any



class QAModel:
    def __init__(
        self,
        model_name: str = "distilbert-base-cased-distilled-squad",
        device: Optional[str] = None
    ):
        """
        Initialize QA model.
        
        Args:
            model_name: HuggingFace model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.pipeline = None
    
    def _get_pipeline(self):
        """Lazy load QA pipeline."""
        if self.pipeline is None:
            try:
                from transformers import pipeline
                self.pipeline = pipeline(
                    "question-answering",
                    model=self.model_name,
                    device=-1 if (self.device or "") == "cpu" else 0
                )
            except ImportError:
                raise ImportError(
                    "transformers not installed. Install with:\n"
                    "  pip install transformers torch"
                )
        return self.pipeline
    
    def answer(
        self,
        question: str,
        context: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Answer a question given context.
        
        Args:
            question: Question to answer.
            context: Context to extract answer from.
            
        Returns:
            Dict with 'answer', 'score', 'start', 'end'.
        """
        pipeline = self._get_pipeline()
        
        result = pipeline(
            question=question,
            context=context,
            **kwargs
        )
        
        return result
    
    def extract_answer(self, question: str, context: str) -> str:
        """
        Extract plain answer text.
        
        Args:
            question: Question.
            context: Context.
            
        Returns:
            Answer text.
        """
        result = self.answer(question, context)
        return result["answer"]


def quick_qa(question: str, context: str) -> str:
    """
    Quick question answering.
    
    Args:
        question: Question.
        context: Context.
        
    Returns:
        Answer.
    """
    qa = QAModel()
    return qa.extract_answer(question, context)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python -m ai.qa <question> <context>")
        sys.exit(1)
    
    question = sys.argv[1]
    context = " ".join(sys.argv[2:])
    
    result = quick_qa(question, context)
    print(f"Answer: {result}")
