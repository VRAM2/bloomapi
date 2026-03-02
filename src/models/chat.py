from sqlalchemy import Column, Integer, String, ForeignKey, Text
from src.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    role = Column(String)
    content = Column(Text)