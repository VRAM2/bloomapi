from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.users import User
    from src.models.sensor_data import SensorData

class Plant(Base):
    __tablename__ = 'plants'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    temp_c: Mapped[int] = mapped_column()
    soil_moisture_pct: Mapped[int] = mapped_column()
    air_humidity_pct: Mapped[int] = mapped_column()
    light_lux: Mapped[int] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="plants")
    sensor_history: Mapped[list["SensorData"]] = relationship(back_populates="plant")