from pydantic import BaseModel, Field

class SensorDataCreate(BaseModel):
    plant_id: int
    user_id: int
    temp_c: float = Field(..., description="Температура в градусах Цельсия")
    soil_moisture_pct: float = Field(..., ge=0, le=100)
    air_humidity_pct: float = Field(..., ge=0, le=100)
    light_lux: float = Field(..., ge=0)
