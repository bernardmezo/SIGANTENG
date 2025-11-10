# backend/app/services/multimodal_pipeline.py
# =================================================================
#
#                    Multimodal Pipeline Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service encapsulates a complex, multi-step AI workflow that
#  combines vision, language, and speech models. It orchestrates the
#  "image-to-poem-to-speech" pipeline.
#
#  Key Features:
#  -------------
#  - Decouples the business logic of the pipeline from the API endpoint.
#  - Injects required AI services for better testability and modularity.
#  - Provides a single, clean method to execute the entire workflow.
#
# =================================================================

import logging
from typing import Any, Dict

from app.models.schemas import AIResponse  # Assuming a shared schema
from app.services.langchain_orchestrator import LangChainOrchestrator
from app.services.tts_service import TTSService
from app.services.vision_service import VisionService

logger = logging.getLogger(__name__)


class MultimodalPipeline:
    """
    Orchestrates the "image-to-poem-to-speech" workflow.
    """

    def __init__(
        self,
        vision_service: VisionService,
        langchain_orchestrator: LangChainOrchestrator,
        tts_service: TTSService,
    ):
        self.vision_service = vision_service
        self.langchain_orchestrator = langchain_orchestrator
        self.tts_service = tts_service

    async def process_image(self, image_base64: str) -> Dict[str, Any]:
        """
        Executes the full image-to-speech pipeline.

        Args:
            image_base64: The base64-encoded image string.

        Returns:
            A dictionary containing the results of the pipeline, including
            the image description, the generated text (poem), and the
            base64-encoded audio.
        """
        logger.info("Starting multimodal pipeline for image processing.")

        # 1. Get image description from Vision Service
        try:
            image_description = await self.vision_service.get_image_description(
                image_base64
            )
            if not image_description:
                logger.warning("Vision service returned no description.")
                raise ValueError("Could not get a description from the image.")
            logger.info(
                f"Vision service succeeded. Description: '{image_description[:50]}...'"
            )
        except Exception as e:
            logger.error(f"Error in vision service step: {e}", exc_info=True)
            raise

        # 2. Generate a poem from the description using LangChain Orchestrator
        try:
            # We create a more creative prompt for the poem generation
            prompt_intro = "Based on the following description of an image, "
            prompt_body = f"write a short, evocative poem: '{image_description}'"
            poem_prompt = prompt_intro + prompt_body
            llm_response = await self.langchain_orchestrator.run_text_pipeline(
                poem_prompt
            )
            generated_text = llm_response.response_text
            if not generated_text:
                logger.warning("LLM service returned no text.")
                raise ValueError("Could not generate text from the description.")
            logger.info(
                f"LLM service succeeded. Generated text: '{generated_text[:50]}...'"
            )
        except Exception as e:
            logger.error(f"Error in LLM service step: {e}", exc_info=True)
            raise

        # 3. Convert the generated poem to speech using TTS Service
        try:
            audio_base64 = await self.tts_service.generate_audio(generated_text)
            if not audio_base64:
                logger.warning("TTS service returned no audio.")
                # This might not be a critical failure, so we don't raise an exception
                # but will return None for the audio.
                pass
            logger.info("TTS service succeeded.")
        except Exception as e:
            logger.error(f"Error in TTS service step: {e}", exc_info=True)
            # Also not a critical failure for the whole pipeline
            audio_base64 = None

        return {
            "image_description": image_description,
            "response_text": generated_text,
            "audio_base64": audio_base64,
            "recommendations": llm_response.recommendations,
        }
