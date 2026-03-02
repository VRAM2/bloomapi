from src.models.users import User
from src.models.plants import Plant
from src.models.sensor_data import SensorData
from src.models.actions import PlantAction
from src.models.chat import ChatMessage
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from src.database import async_session

async def create_user(username: str, password_hash: str):
    async with async_session() as session:
        db_user = User(username=username, password_hash=password_hash)
        session.add(db_user)
        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except IntegrityError:
            await session.rollback()
            return False

async def get_user_by_username(username: str):
    async with async_session() as session:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalars().first()

async def delete_user(user_id: int):
    async with async_session() as session:
        plant_ids_query = select(Plant.id).where(Plant.user_id == user_id)
        plant_ids_result = await session.execute(plant_ids_query)
        plant_ids = [plant_id[0] for plant_id in plant_ids_result.fetchall()]
        
        if plant_ids:
            chat_query = select(ChatMessage).where(ChatMessage.plant_id.in_(plant_ids))
            chat_result = await session.execute(chat_query)
            for chat_message in chat_result.scalars().all():
                await session.delete(chat_message)

        action_query = select(PlantAction).where(PlantAction.user_id == user_id)
        action_result = await session.execute(action_query)
        for action in action_result.scalars().all():
            await session.delete(action)

        sensor_query = select(SensorData).where(SensorData.user_id == user_id)
        sensor_result = await session.execute(sensor_query)
        for sensor_data in sensor_result.scalars().all():
            await session.delete(sensor_data)

        plant_query = select(Plant).where(Plant.user_id == user_id)
        plant_result = await session.execute(plant_query)
        for plant in plant_result.scalars().all():
            await session.delete(plant)

        user_query = select(User).where(User.id == user_id)
        user_result = await session.execute(user_query)
        user = user_result.scalars().first()
        if user:
            await session.delete(user)
        
        await session.commit()
        return True
    return False
