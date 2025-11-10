# backend/app/services/langchain_orchestrator.py
# =================================================================
#
#                  LangChain Orchestrator Service
#
# =================================================================
#
#  Purpose:
#  --------
#  This service was originally designed to orchestrate complex
#  interactions using LangChain agents. After refactoring core model
#  interactions into adapters, this service's role is simplified.
#
#  Current Role:
#  -------------
#  - Acts as a high-level coordinator for processing text input.
#  - Uses the LLMService to generate a primary response.
#  - (Future) Can be expanded to re-introduce more complex agentic
#    workflows using the new adapter-based services.
#
# =================================================================

from app.models.schemas import ChatResponse
from app.services.llm_service import LLMService
from app.services.recommendation_service import RecommendationService


class LangChainOrchestrator:
    """
    Orchestrates NLP tasks, using various services.
    NOTE: The 'LangChain' name is kept for now, but its role is simplified
    to use the new adapter-based LLMService.
    """

    def __init__(self):
        self.llm_service = LLMService(provider="huggingface")
        self.recommendation_service = RecommendationService()
        # The agent is temporarily disabled in favor of a direct service call.
        # self.agent_executor = self._initialize_agent()

    async def run_text_pipeline(self, text: str) -> ChatResponse:
        """
        Processes text by generating a response from the LLM and
        fetching recommendations.

        Args:
            text: The user's input text.

        Returns:
            A ChatResponse object containing the response and recommendations.
        """
        try:
            # Generate the main text response using the LLM service
            response_text = await self.llm_service.generate_response(text)

            # Get recommendations based on the input text
            recommendations = await self.recommendation_service.get_recommendations(
                text
            )

            return ChatResponse(
                response_text=response_text, recommendations=recommendations
            )
        except Exception as e:
            print(f"Error running text pipeline: {e}")
            return ChatResponse(
                response_text=f"Sorry, there was an error processing your request: {e}"
            )
