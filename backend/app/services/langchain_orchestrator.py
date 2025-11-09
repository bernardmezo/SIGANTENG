from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.tools import tool

from app.services.nlp_service import NLPService
from app.services.recommendation_service import RecommendationService
from app.models.schemas import ChatResponse

class LangChainOrchestrator:
    def __init__(self):
        self.nlp_service = NLPService()
        self.recommendation_service = RecommendationService()
        self.llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta", 
                                  task="text-generation", 
                                  model_kwargs={
                                      "temperature": 0.7,
                                      "max_new_tokens": 500
                                  })
        self.agent_executor = self._initialize_agent()

    @tool
    async def get_recommendations(self, query: str) -> list[str]:
        """Use this tool to get recommendations based on a user query. Input should be a string query."""
        return await self.recommendation_service.get_recommendations(query)

    def _initialize_agent(self) -> AgentExecutor:
        tools = [self.get_recommendations]
        
        # Define the prompt for the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Use the available tools to answer questions and provide recommendations."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        # Create the ReAct agent
        agent = create_react_agent(self.llm, tools, prompt)
        
        # Create the agent executor
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor

    async def run_text_pipeline(self, text: str) -> ChatResponse:
        # First, process text with NLP for initial understanding or sentiment
        # nlp_result = await self.nlp_service.process_text(text)

        # Then, use the LangChain agent for more complex reasoning and tool usage
        try:
            agent_response = await self.agent_executor.ainvoke({"input": text})
            # The agent_response will contain the output from the LLM after using tools
            # You might need to parse this output based on how your agent is configured
            
            response_text = agent_response.get("output", "No specific response from AI.")
            recommendations = [] # Populate if agent explicitly returns recommendations

            # Example of how you might extract recommendations if the agent's output format is known
            if "recommendation" in response_text.lower():
                # This is a placeholder, actual parsing would depend on agent's output
                recommendations.append("Extracted a potential recommendation from agent output.")

            return ChatResponse(response_text=response_text, recommendations=recommendations)
        except Exception as e:
            print(f"Error running LangChain agent: {e}")
            return ChatResponse(response_text=f"Error processing your request: {e}")
