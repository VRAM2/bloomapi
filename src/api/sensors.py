from fastapi import APIRouter, HTTPException
from src.schemas.sensor_data import SensorDataCreate
from src.services.sensors import save_sensor_readings

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/report")
async def report_sensor_data(payload: SensorDataCreate):
    success = await save_sensor_readings(payload)
    if success:
        return {"status": "ok", "message": "Данные успешно сохранены"}
    raise HTTPException(status_code=500, detail="Ошибка при сохранении данных")