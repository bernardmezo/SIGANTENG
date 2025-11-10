# backend/app/api/v1/endpoints/ai_assistant.py
from app.services.ai_orchestrator import AIOrchestratorService
from app.services.langchain_orchestrator import LangChainOrchestrator
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.services.vision_service import VisionService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# --- Dependency Injection Providers ---


def get_langchain_orchestrator() -> LangChainOrchestrator:
    return LangChainOrchestrator()


def get_stt_service() -> STTService:
    return STTService()


def get_vision_service() -> VisionService:
    return VisionService()


def get_tts_service() -> TTSService:
    return TTSService()


def get_ai_orchestrator() -> AIOrchestratorService:
    return AIOrchestratorService()


# --- Pydantic Models ---


class TextInput(BaseModel):
    text: str


class AudioInput(BaseModel):
    audio_base64: str


class ImageInput(BaseModel):
    image_base64: str


class AIResponse(BaseModel):
    response_text: str | None = None
    recommendations: list[str] | None = None
    audio_base64: str | None = None


class TaskSubmissionResponse(BaseModel):
    task_id: str
    status: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: str | None = None


# --- Synchronous Endpoints (Existing) ---


@router.post("/process_text", response_model=AIResponse)
async def process_text_input(
    input: TextInput,
    langchain_orchestrator: LangChainOrchestrator = Depends(get_langchain_orchestrator),
    tts_service: TTSService = Depends(get_tts_service),
):
    response = await langchain_orchestrator.run_text_pipeline(input.text)
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.generate_audio(response.response_text)
    return AIResponse(
        response_text=response.response_text,
        recommendations=response.recommendations,
        audio_base64=audio_base64,
    )


@router.post("/process_audio", response_model=AIResponse)
async def process_audio_input(
    input: AudioInput,
    stt_service: STTService = Depends(get_stt_service),
    langchain_orchestrator: LangChainOrchestrator = Depends(get_langchain_orchestrator),
    tts_service: TTSService = Depends(get_tts_service),
):
    text = await stt_service.transcribe_audio(input.audio_base64)
    if not text:
        raise HTTPException(status_code=400, detail="Could not convert audio to text")
    response = await langchain_orchestrator.run_text_pipeline(text)
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.generate_audio(response.response_text)
    return AIResponse(
        response_text=response.response_text,
        recommendations=response.recommendations,
        audio_base64=audio_base64,
    )


@router.post("/process_image", response_model=AIResponse)
async def process_image_input(
    input: ImageInput,
    vision_service: VisionService = Depends(get_vision_service),
    langchain_orchestrator: LangChainOrchestrator = Depends(get_langchain_orchestrator),
    tts_service: TTSService = Depends(get_tts_service),
):
    image_description = await vision_service.get_image_description(input.image_base64)
    if not image_description:
        raise HTTPException(status_code=400, detail="Could not understand image")
    response = await langchain_orchestrator.run_text_pipeline(
        f"Analyze this image: {image_description}"
    )
    audio_base64 = None
    if response.response_text:
        audio_base64 = await tts_service.generate_audio(response.response_text)
    return AIResponse(
        response_text=response.response_text,
        recommendations=response.recommendations,
        audio_base64=audio_base64,
    )


# --- Asynchronous Background Task Endpoints (New) ---


@router.post(
    "/background/generate_text",
    response_model=TaskSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit_text_generation_task(
    input: TextInput,
    ai_orchestrator: AIOrchestratorService = Depends(get_ai_orchestrator),
):
    task_id = ai_orchestrator.submit_long_llm_generation(input.text)
    return JSONResponse(
        content={"task_id": task_id, "status": "PENDING"},
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.get("/background/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str, ai_orchestrator: AIOrchestratorService = Depends(get_ai_orchestrator)
):
    task_info = ai_orchestrator.get_task_status_and_result(task_id)
    return task_info
