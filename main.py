from fastapi import FastAPI, HTTPException
import httpx
import logging
import redis
from redis_client import get_request_response, store_request_response
from models import InputData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка клиента Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.post("/process_data/")
async def process_data(input_data: InputData):
    try:
        # Логируем входящие данные
        logger.info(f"Received data: {input_data}")
        request_id = input_data.data.get('cat')
        cached_data = await get_request_response(request_id)
        if cached_data:
            return {"input_data": input_data, "cat_fact": cached_data}
        # Асинхронный запрос к публичному API
        async with httpx.AsyncClient() as client:
            response = await client.get("https://catfact.ninja/fact")
            response.raise_for_status()
            cat_fact = response.json().get("fact")

        # Сохранение данных в Redis
        await redis_client.set(input_data["id"], cat_fact)  # Предполагаем, что в входных данных есть поле 'id'

        # Возвращаем результат
        return {"input_data": input_data, "cat_fact": cat_fact}

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")