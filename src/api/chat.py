from fastapi import APIRouter, Depends
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
service = ChatService()

@router.get("/history/{plant_id}")
async def get_history(plant_id: int):
    history = await service.get_history(plant_id)
    return [{"role": m.role, "content": m.content} for m in history]

@router.post("/send", response_model=ChatResponse)
async def send_message(req: ChatRequest):
    content = await service.generate_response(req.plant_id, req.message)
    return ChatResponse(role="assistant", content=content)