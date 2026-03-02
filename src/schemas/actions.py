from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActionReport(BaseModel):
    plant_id: int
    action: str
    state: bool

class ActionLogResponse(BaseModel):
    id: int
    action_type: str
    started_at: datetime
    ended_at: Optional[datetime]
    class Config:
        from_attributes = True