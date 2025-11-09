import base64
from gtts import gTTS
from io import BytesIO

class TTSService:
    def __init__(self):
        pass

    async def text_to_speech(self, text: str) -> str:
        try:
            tts = gTTS(text=text, lang='en') # Default to English
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Encode audio to base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            return audio_base64
        except Exception as e:
            print(f"Error converting text to speech: {e}")
            return ""
