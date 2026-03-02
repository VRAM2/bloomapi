from mistralai import Mistral
from sqlalchemy import select, desc
from src.database import async_session
from src.models.chat import ChatMessage
from src.models.plants import Plant
from src.models.sensor_data import SensorData

class ChatService:
    def __init__(self):
        self.client = Mistral(api_key="wm3nHnZSRVDdA924xJyIW1E1wxWYqE5V")

    async def get_history(self, plant_id: int):
        async with async_session() as session:
            query = select(ChatMessage).where(ChatMessage.plant_id == plant_id).order_by(ChatMessage.id)
            result = await session.execute(query)
            return result.scalars().all()

    async def generate_response(self, plant_id: int, user_message: str):
        async with async_session() as session:
            plant_query = select(Plant).where(Plant.id == plant_id)
            plant = (await session.execute(plant_query)).scalars().first()
            
            sensor_query = select(SensorData).where(SensorData.plant_id == plant_id).order_by(desc(SensorData.id)).limit(1)
            sensors = (await session.execute(sensor_query)).scalars().first()

            history_query = select(ChatMessage).where(ChatMessage.plant_id == plant_id).order_by(desc(ChatMessage.id)).limit(10)
            history_db = (await session.execute(history_query)).scalars().all()
            
            history = [{"role": m.role, "content": m.content} for m in reversed(history_db)]

            system_prompt = f"Ты помощник-бот по уходу за растением {plant.name}. "
            system_prompt += f"Идеал: температура воздуха {plant.temp_c}C, влажность почвы {plant.soil_moisture_pct}%, влажность воздуха {plant.air_humidity_pct}%, освещенность {plant.light_lux} lux. "
            if sensors:
                system_prompt += f"Текущие: температура воздуха {sensors.temp_c}C, влажность почвы {sensors.soil_moisture_pct}%, влажность воздуха {sensors.air_humidity_pct}%, освещенность {sensors.light_lux} lux. "
            
            system_prompt += "Не используй **Слово** и тд, для изменения курсива, жирности текста и тд. В чате это не работает"
            messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_message}]

            user_msg = ChatMessage(plant_id=plant_id, role="user", content=user_message)
            session.add(user_msg)
            await session.commit()

            response = self.client.chat.complete(model="mistral-small-latest", messages=messages)
            ai_content = response.choices[0].message.content

            ai_msg = ChatMessage(plant_id=plant_id, role="assistant", content=ai_content)
            session.add(ai_msg)
            await session.commit()

            return ai_content