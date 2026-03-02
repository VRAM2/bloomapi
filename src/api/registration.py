from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from src.auth_utils import get_password_hash, create_access_token
from src.services.users import create_user, get_user_by_username
from src.schemas.users import UserCreate

router = APIRouter()

@router.post("/registration", tags=["User"], summary="Регистрация пользователя")
async def registration(user: UserCreate):
    if await get_user_by_username(user.username): 
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
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