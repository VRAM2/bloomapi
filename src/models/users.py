from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from sqlalchemy import func
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.plants import Plant
    from src.models.sensor_data import SensorData

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    
    plants: Mapped[list["Plant"]] = relationship(back_populates="user")
    sensor_readings: Mapped[list["SensorData"]] = relationship(back_populates="user")