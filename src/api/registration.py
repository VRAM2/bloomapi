from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from src.auth_utils import get_password_hash, create_access_token
from src.services.users import create_user, delete_user
from sqlalchemy import select
from src.database import async_session
from src.models.users import User
from src.schemas.users import UserCreate

router = APIRouter()

@router.post("/registration", tags=["User"], summary="Регистрация пользователя")
async def registration(user: UserCreate):
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for u in users:
            await delete_user(u.id)
    
    new_user = await create_user(user.username, get_password_hash(user.password))
    access_token = create_access_token(data={"sub": new_user.username})
    
    if new_user: 
        return {
            "success": True, 
            "message": "Пользователь успешно зарегистрирован",
            "user_id": new_user.id,
            "access_token": access_token
        }
    raise HTTPException(status_code=500, detail="Ошибка при регистрации")
