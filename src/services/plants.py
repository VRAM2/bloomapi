import json
import re
from mistralai import Mistral
from src.database import async_session
from src.models.plants import Plant
from sqlalchemy import select
from src.models.sensor_data import SensorData

api_key = "wm3nHnZSRVDdA924xJyIW1E1wxWYqE5V"
client = Mistral(api_key=api_key, server_url="https://api.mistral.ai")

PROMPT_TEMPLATE = """Роль: Эксперт-ботаник и инженер систем автоматизации умных оранжерей.
Задача: Обработай список из 3 названий растений для базы данных.
Инструкции:
1. Исправление названия: Исправь орфографические ошибки и напиши полное официальное биологическое название на русском языке, например, с Мухаловка на Венерина Мухоловка, с Денежного дерева на Толстянку и тд. Без латыни и без скобок. Начинаться должно с заглавной буквы.
2. Классификация: Определи тип растения: plant, flower или tree (напиши строго на английском).
3. Параметры (точные целые числа): Укажи одно оптимальное значение в виде числа (не используй диапазоны вроде "20-30"):
- Температура воздуха: в градусах Цельсия.
- Влажность почвы: в процентах.
- Влажность воздуха: в процентах.
- Освещенность: в дипазоне от 0 до 4095, где 0 - темно, 4095-ярко. это не какая то величина, типа люксов, просто такой вот диапазон, но ты должен дать точное число. записать в light_lux, хотя это и не люксы.

Формат ответа: Верни результат строго в формате JSON. Не добавляй никаких вступительных слов или пояснений. В ответе не должно быть оригинальных (ошибочных) имен.

Список растений для обработки:
{plant_names}

Структура JSON:
{{
    "greenhouse_data": [
        {{
            "name": "Исправленное название на русском",
            "type": "plant/flower/tree",
            "requirements": {{
                "temp_c": 24,
                "soil_moisture_pct": 60,
                "air_humidity_pct": 55,
                "light_lux": 5000
            }}
        }}
    ]
}}
"""

async def generate_and_save_plants(user_id: int, plant_names_list: list[str]):
    prompt = PROMPT_TEMPLATE.format(plant_names="\n".join(plant_names_list))

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        raw_data = response.choices[0].message.content
        clean_json = re.sub(r"```json|```", "", raw_data).strip()
        data = json.loads(clean_json)

        async with async_session() as session:
            for item in data["greenhouse_data"]:
                plant = Plant(
                    user_id=user_id,
                    name=item["name"],
                    type=item["type"],
                    temp_c=item["requirements"]["temp_c"],
                    soil_moisture_pct=item["requirements"]["soil_moisture_pct"],
                    air_humidity_pct=item["requirements"]["air_humidity_pct"],
                    light_lux=item["requirements"]["light_lux"]
                )
                session.add(plant)

            await session.commit()
            return True
    except Exception as e:
        print(f"Error processing AI response: {e}")
        return False

async def get_plants_by_user(user_id: int):
    async with async_session() as session:
        query = select(Plant).where(Plant.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

def calc_status(plant, sensor: SensorData | None, has_action: bool):
    if has_action:
        return "action"

    if not sensor:
        return "attention"

    problems = 0

    def check(value, optimal, delta):
        return abs(value - optimal) > delta * 2

    if check(sensor.temp_c, plant.temp_c, 3):
        problems += 1
    if check(sensor.soil_moisture_pct, plant.soil_moisture_pct, 15):
        problems += 1
    if check(sensor.air_humidity_pct, plant.air_humidity_pct, 15):
        problems += 1
    if check(sensor.light_lux, plant.light_lux, plant.light_lux * 0.3):
        problems += 1

    return "attention" if problems >= 2 else "ok"

async def get_plant_by_id(plant_id: int):
    async with async_session() as session:
        query = select(Plant).where(Plant.id == plant_id)
        result = await session.execute(query)
        return result.scalars().first()