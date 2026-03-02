from fastapi import APIRouter

from src.api.registration import router as registration_router
from src.api.auth import router as auth_router
from src.api.plantsseed import router as plantsseed_router
from src.api.user import router as user_router
from src.api.sensors import router as sensor_router
from src.api.actions import router as actions_router
from src.api.chat import router as chat_router

main_router = APIRouter()

main_router.include_router(registration_router)
main_router.include_router(auth_router)
main_router.include_router(plantsseed_router)
main_router.include_router(user_router)
main_router.include_router(sensor_router)
main_router.include_router(actions_router)
main_router.include_router(chat_router)

