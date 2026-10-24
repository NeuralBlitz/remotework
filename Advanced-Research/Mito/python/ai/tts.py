"""
Text-to-Speech using Coqui TTS
"""

from typing import Optional
from pathlib import Path



class TTSEngine:
    def __init__(
        self,
        model_name: str = "tts_models/en/ljspeech/glow-tts",
        device: Optional[str] = None
    ):
        """
        Initialize TTS engine.
        
        Args:
            model_name: TTS model name.
            device: Device to use.
        """
        self.model_name = model_name
        self.device = device
        self.model = None
    
    def _get_model(self):
        """Lazy load TTS model."""
        if self.model is None:
            try:
                from TTS.api import TTS
                self.model = TTS(
                    model_name=self.model_name,
                    device=self.device or "cpu"
                )
            except ImportError:
                raise ImportError(
                    "TTS not installed. Install with:\n"
                    "  pip install TTS"
                )
        return self.model
    
    def speak(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Convert text to speech.
        
        Args:
            text: Text to speak.
            output_path: Output file path.
            
        Returns:
            Path to generated audio file.
        """
        model = self._get_model()
        
        if output_path is None:
            output_path = "output.wav"
        
        model.tts(text, file_path=output_path, **kwargs)
        
        return output_path
    
    def speak_to_file(
        self,
        text: str,
        output_file: str,
        **kwargs
    ) -> str:
        """
        Save speech to file.
        
        Args:
            text: Text to speak.
            output_file: Output file path.
            
        Returns:
            Path to generated audio.
        """
        return self.speak(text, output_file, **kwargs)


def quick_speak(text: str, output: str = "speech.wav") -> str:
    """
    Quick text-to-speech.
    
    Args:
        text: Text to speak.
        output: Output file.
        
    Returns:
        Output file path.
    """
    tts = TTSEngine()
    return tts.speak(text, output)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m ai.tts <text> [output_file]")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    output = sys.argv[2] if len(sys.argv) > 2 else "speech.wav"
    
    print(f"Generating speech for: {text}")
    result = quick_speak(text, output)
    print(f"Saved to: {result}")
