from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
from src.database import Base
import datetime

class PlantAction(Base):
    __tablename__ = 'plant_actions'
    id: Mapped[int] = mapped_column(primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action_type: Mapped[str] = mapped_column()
    started_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    ended_at: Mapped[datetime.datetime] = mapped_column(nullable=True)