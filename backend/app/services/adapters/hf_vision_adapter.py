# backend/app/services/adapters/hf_vision_adapter.py
# =================================================================
#
#                 Hugging Face Vision Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseVisionAdapter for Hugging Face
#  models. This adapter uses the `transformers` pipeline for
#  image-to-text tasks.
#
#  Key Features:
#  -------------
#  - Initializes a Hugging Face image-to-text pipeline.
#  - Implements `get_image_description` to generate captions.
#  - Runs the synchronous pipeline in a thread for async safety.
#
# =================================================================

import asyncio
import base64
from io import BytesIO

from app.core.config import settings
from app.services.base.vision_adapter import BaseVisionAdapter
from transformers import pipeline


class HuggingFaceVisionAdapter(BaseVisionAdapter):
    """Adapter for Hugging Face image-to-text models."""

    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        self.pipeline = pipeline(
            "image-to-text",
            model=model_name,
            token=settings.HF_API_TOKEN,
        )

    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for a base64-encoded image.

        Args:
            image_base64: The base64-encoded image string.

        Returns:
            A textual description of the image.
        """
        try:
            image_bytes = base64.b64decode(image_base64)
            image_file = BytesIO(image_bytes)

            # Run the synchronous pipeline in a separate thread
            result = await asyncio.to_thread(self.pipeline, image_file)
            return result[0]["generated_text"]
        except Exception as e:
            print(f"Error getting image description from HuggingFace: {e}")
            return "Could not generate a description for the image."
