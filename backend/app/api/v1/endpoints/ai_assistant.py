from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.langchain_orchestrator import LangChainOrchestrator
from app.services.stt_service import STTService
from app.services.vision_service import VisionService
from app.services.tts_service import TTSService

router = APIRouter()

# Initialize services (can be dependency injected in a real app)
langchain_orchestrator = LangChainOrchestrator()
stt_service = STTService()
vision_service = VisionService()
tts_service = TTSService()

class TextInput(BaseModel:
    text: str

class AudioInput(BaseModel:
    audio_base64: str # Base64 encoded audio data

class ImageInput(BaseModel:
    image_base64: str # Base64 encoded image data

class AIResponse(BaseModel:
    response_text: str | None = None
    recommendations: list[str] | None = None
    audio_base64: str | None = None # Base64 encoded audio response

@router.post("/process_text", response_model=AIResponse)
async def process_text_input(input: TextInput):
    # Orchestrate with LangChain for NLP and Reasoning
    response = await langchain_orchestrator.run_text_pipeline(input.text)
    # Potentially generate TTS response
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.text_to_speech(response.response_text)
    return AIResponse(response_text=response.response_text, recommendations=response.recommendations, audio_base64=audio_base64)

@router.post("/process_audio", response_model=AIResponse)
async def process_audio_input(input: AudioInput):
    # STT to convert audio to text
    text = await stt_service.speech_to_text(input.audio_base64)
    if not text:
        raise HTTPException(status_code=400, detail="Could not convert audio to text")

    # Orchestrate with LangChain for NLP and Reasoning
    response = await langchain_orchestrator.run_text_pipeline(text)
    # Potentially generate TTS response
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.text_to_speech(response.response_text)
    return AIResponse(response_text=response.response_text, recommendations=response.recommendations, audio_base64=audio_base64)

@router.post("/process_image", response_model=AIResponse)
async def process_image_input(input: ImageInput):
    # Vision model to understand image
    image_description = await vision_service.understand_image(input.image_base64)
    if not image_description:
        raise HTTPException(status_code=400, detail="Could not understand image")

    # Orchestrate with LangChain for reasoning based on image description
    response = await langchain_orchestrator.run_text_pipeline(f"Analyze this image: {image_description}")
    # Potentially generate TTS response
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.text_to_speech(response.response_text)
    return AIResponse(response_text=response.response_text, recommendations=response.recommendations, audio_base64=audio_base64)
