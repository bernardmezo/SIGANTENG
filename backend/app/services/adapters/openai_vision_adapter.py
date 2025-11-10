# backend/app/services/adapters/openai_vision_adapter.py
# =================================================================
#
#                   OpenAI Vision Adapter
#
# =================================================================
#
#  Purpose:
#  --------
#  Concrete implementation of the BaseVisionAdapter for OpenAI's
#  multimodal models like GPT-4o.
#
#  Key Features:
#  -------------
#  - Uses `openai.AsyncOpenAI` for non-blocking API requests.
#  - Implements `get_image_description` by sending a base64-encoded
#    image to the chat completions endpoint.
#
# =================================================================

from app.core.config import settings
from app.services.base.vision_adapter import BaseVisionAdapter
from openai import AsyncOpenAI


class OpenAIVisionAdapter(BaseVisionAdapter):
    """Adapter for OpenAI's multimodal models (e.g., GPT-4o)."""

    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for a base64-encoded image using a
        multimodal OpenAI model.

        Args:
            image_base64: The base64-encoded image string.

        Returns:
            A textual description of the image.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What’s in this image?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=100,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting image description from OpenAI: {e}")
            return "Could not generate a description for the image."
