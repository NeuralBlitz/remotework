"""
Speech Recognition using Whisper
"""

from typing import Optional, List, Dict, Any



class SpeechRecognizer:
    def __init__(
        self,
        model_name: str = "base",
        device: Optional[str] = None,
        language: Optional[str] = None
    ):
        """
        Initialize speech recognizer.
        
        Args:
            model_name: Whisper model size (tiny, base, small, medium, large).
            device: Device to use ('cuda', 'cpu').
            language: Specific language code (e.g., 'en', 'es').
        """
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model = None
    
    def _get_model(self):
        """Lazy load Whisper model."""
        if self.model is None:
            try:
                import whisper
                self.model = whisper.load_model(self.model_name, device=self.device or "cpu")
            except ImportError:
                raise ImportError(
                    "openai-whisper not installed. Install with:\n"
                    "  pip install openai-whisper"
                )
        return self.model
    
    def transcribe(
        self,
        audio_path: str,
        verbose: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file.
            verbose: Enable verbose output.
            
        Returns:
            Dict with 'text', 'segments', 'language'.
        """
        model = self._get_model()
        
        result = model.transcribe(
            audio_path,
            language=self.language,
            verbose=verbose,
            **kwargs
        )
        
        return result
    
    def transcribe_batch(
        self,
        audio_paths: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Transcribe multiple audio files.
        
        Args:
            audio_paths: List of audio file paths.
            
        Returns:
            List of transcription results.
        """
        results = []
        for path in audio_paths:
            results.append(self.transcribe(path, **kwargs))
        return results
    
    def get_text(self, audio_path: str) -> str:
        """
        Get plain text from audio.
        
        Args:
            audio_path: Path to audio file.
            
        Returns:
            Transcribed text.
        """
        result = self.transcribe(audio_path)
        return result["text"]


def quick_transcribe(audio_path: str, model: str = "base") -> str:
    """
    Quick transcription.
    
    Args:
        audio_path: Path to audio file.
        model: Model size.
        
    Returns:
        Transcribed text.
    """
    recognizer = SpeechRecognizer(model_name=model)
    return recognizer.get_text(audio_path)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.speech <audio_file> [model]")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    
    print(f"Transcribing: {audio_path}")
    print(f"Model: {model}")
    
    text = quick_transcribe(audio_path, model)
    print(f"\nTranscription:\n{text}")
