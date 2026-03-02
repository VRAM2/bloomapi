from pydantic import BaseModel

class ChatRequest(BaseModel):
    plant_id: int
    message: str

class ChatResponse(BaseModel):
    role: str
    content: str