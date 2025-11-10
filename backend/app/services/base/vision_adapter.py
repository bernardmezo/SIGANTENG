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
    """Abstract base class for Vision adapters."""

    @abstractmethod
    async def get_image_description(self, image_base64: str) -> str:
        """
        Generates a description for a single image.
        """
        pass

    async def get_image_descriptions_batch(self, images_base64: list[str]) -> list[str]:
        """
        Generates descriptions for a batch of images.

        NOTE: This is a non-optimized default implementation.
        Subclasses should override this method to leverage true batch
        inference capabilities of the underlying model if available.
        """
        return [await self.get_image_description(image) for image in images_base64]
