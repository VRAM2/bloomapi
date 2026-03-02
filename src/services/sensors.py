from src.database import async_session
from src.models.sensor_data import SensorData
from src.schemas.sensor_data import SensorDataCreate
from sqlalchemy import desc, select

async def save_sensor_readings(data: SensorDataCreate):
    async with async_session() as session:
        new_reading = SensorData(
            plant_id=data.plant_id,
            user_id=data.user_id,
            temp_c=data.temp_c,
            soil_moisture_pct=data.soil_moisture_pct,
            air_humidity_pct=data.air_humidity_pct,
            light_lux=data.light_lux
        )
        session.add(new_reading)
        await session.commit()
        return True
    
async def get_latest_sensor_data(plant_id: int):
    async with async_session() as session:
        query = (
            select(SensorData)
            .where(SensorData.plant_id == plant_id)
            .order_by(desc(SensorData.timestamp))
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalars().first()