from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from src.database import Base 
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.plants import Plant 
    from src.models.users import User

class SensorData(Base): 
    __tablename__ = 'sensor_data'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id")) 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
    
    temp_c: Mapped[float] = mapped_column()
    soil_moisture_pct: Mapped[float] = mapped_column()
    air_humidity_pct: Mapped[float] = mapped_column()
    light_lux: Mapped[float] = mapped_column()
    timestamp: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    plant: Mapped["Plant"] = relationship(back_populates="sensor_history")
    user: Mapped["User"] = relationship(back_populates="sensor_readings")