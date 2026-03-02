from fastapi import APIRouter, Depends, HTTPException
from src.api.auth import get_current_user
from src.models.users import User
from src.services.users import delete_user

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }

@router.delete("/me")
async def delete_me(current_user: User = Depends(get_current_user)):
    success = await delete_user(current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
