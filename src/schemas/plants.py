from pydantic import BaseModel, Field

class PlantRequest(BaseModel):
    user_id: int = Field(..., description="ID пользователя из таблицы users")
    plant_names: list[str] = Field(..., min_items=3, max_items=3)

class PlantResponse(BaseModel):
    id: int
    name: str
    type: str
    temp_c: int
    soil_moisture_pct: int
    air_humidity_pct: int
    light_lux: int

    class Config:
        from_attributes = True