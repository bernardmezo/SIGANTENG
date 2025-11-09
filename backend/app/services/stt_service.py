import base64
from io import BytesIO
from transformers import pipeline

from app.core.config import settings

class STTService:
    def __init__(self):
        # Initialize Whisper model from Hugging Face
        # For larger models or local deployment, consider using a dedicated inference endpoint
        self.asr_pipeline = pipeline(
            "automatic-speech-recognition", 
            model="openai/whisper-tiny", # Using a smaller model for demonstration
            token=settings.HF_API_TOKEN
        )

    async def speech_to_text(self, audio_base64: str) -> str:
        try:
            # Decode base64 audio to bytes
            audio_bytes = base64.b64decode(audio_base64)
            audio_file = BytesIO(audio_bytes)
            
            # Perform speech-to-text
            result = self.asr_pipeline(audio_file)
            return result["text"]
        except Exception as e:
            print(f"Error converting speech to text: {e}")
            return ""
