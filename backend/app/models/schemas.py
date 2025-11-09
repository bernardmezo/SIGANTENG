from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatResponse(BaseModel):
    response_text: str | None = None
    recommendations: list[str] | None = None
