# backend/app/services/base/vision_adapter.py
# =================================================================
#
#                     Vision Adapter Base Class
#
# =================================================================
#
#  Purpose:
#  --------
#  Defines the abstract base class for all computer vision model
#  adapters. This ensures a consistent interface for processing
#  images, such as generating descriptions or captions.
#
#  Key Methods:
#  ------------
#  - get_image_description: An asynchronous method that takes a
#    base64-encoded image string and returns a textual description.
#
# =================================================================

from abc import ABC, abstractmethod


class BaseVisionAdapter(ABC):
    """Abstract base class for Vision model adapters."""

    @abstractmethod
    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for a given base64-encoded image.

        Args:
            image_base64: The base64-encoded string of the image.

        Returns:
            A textual description of the image.
        """
        pass
