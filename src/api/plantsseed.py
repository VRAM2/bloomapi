from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy import select, desc

from src.api.auth import get_current_user 
from src.models.users import User
from src.schemas.plants import PlantRequest, PlantResponse
from src.services.plants import generate_and_save_plants, get_plant_by_id, get_plants_by_user
from src.database import async_session
from src.models.plants import Plant
from src.models.sensor_data import SensorData
from src.services.plants import calc_status
from src.api.actions import ACTIVE_ACTIONS
from src.services.sensors import get_latest_sensor_data


router = APIRouter(prefix="/plants", tags=["Plants"])

@router.get("/", response_model=list[PlantResponse])
async def get_my_plants(current_user: User = Depends(get_current_user)):

    plants = await get_plants_by_user(current_user.id)
    return plants


@router.post("/plantsseed")
async def add_plants_via_ai(
    payload: PlantRequest, 
    current_user: User = Depends(get_current_user) 
):
    success = await generate_and_save_plants(
        user_id=current_user.id, 
        plant_names_list=payload.plant_names
    )
    
    if success:
        return {"success": True, "message": "Растения успешно добавлены"}
    
    raise HTTPException(status_code=500, detail="Ошибка при генерации")

@router.get("/status")
async def get_plants_with_status(current_user: User = Depends(get_current_user)):
    async with async_session() as session:
        plants = await session.execute(
            select(Plant).where(Plant.user_id == current_user.id)
        )
        plants = plants.scalars().all()

        response = []

        for plant in plants:
            sensor_result = await session.execute(
                select(SensorData)
                .where(SensorData.plant_id == plant.id)
                .order_by(desc(SensorData.timestamp))
                .limit(1)
            )
            sensor = sensor_result.scalar_one_or_none()

            has_action = plant.id in ACTIVE_ACTIONS


            status = calc_status(plant, sensor, has_action)

            response.append({
                "id": plant.id,
                "name": plant.name,
                "type": plant.type,
                "status": status
            })

        return response


@router.get("/{plant_id}/details")
async def get_plant_details(plant_id: int, current_user: User = Depends(get_current_user)):
    plant = await get_plant_by_id(plant_id)
    if not plant or plant.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Растение не найдено")
    
    latest_data = await get_latest_sensor_data(plant_id)
    
    return {
        "plant": plant,
        "latest_sensors": latest_data
    }