from fastapi import APIRouter, Depends, HTTPException
from src.schemas.actions import ActionReport, ActionLogResponse
from src.models.actions import PlantAction
from src.api.auth import get_current_user
from src.models.users import User
from src.database import async_session
from sqlalchemy import select, desc
from datetime import datetime

router = APIRouter(prefix="/actions", tags=["Actions"])
ACTIVE_ACTIONS = {}

@router.post("/report")
async def report_action(payload: ActionReport, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        if payload.state:
            ACTIVE_ACTIONS[payload.plant_id] = {
                "action": payload.action,
                "since": datetime.utcnow()
            }
            new_action = PlantAction(
                plant_id=payload.plant_id,
                user_id=current_user.id,
                action_type=payload.action,
                started_at=datetime.utcnow()
            )
            session.add(new_action)
        else:
            ACTIVE_ACTIONS.pop(payload.plant_id, None)
            query = select(PlantAction).where(
                PlantAction.plant_id == payload.plant_id,
                PlantAction.action_type == payload.action,
                PlantAction.ended_at == None
            ).order_by(desc(PlantAction.started_at)).limit(1)
            result = await session.execute(query)
            db_action = result.scalar_one_or_none()
            if db_action:
                db_action.ended_at = datetime.utcnow()
        await session.commit()
    return {"status": "ok"}

@router.get("/journal/{plant_id}", response_model=list[ActionLogResponse])
async def get_journal(plant_id: int, current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        query = select(PlantAction).where(
            PlantAction.plant_id == plant_id,
            PlantAction.user_id == current_user.id
        ).order_by(desc(PlantAction.started_at))
        result = await session.execute(query)
        return result.scalars().all()