import redis.asyncio as redis
import json

redis_client: redis.Redis = None  # Global Redis instance

async def store_request_response(key: str, data: dict):
    """
    Stores request-response data in Redis.
    """
    global redis_client
    await redis_client.set(key, json.dumps(data))

async def get_request_response(key: str):
    """
    Retrieves request-response data from Redis.
    """
    global redis_client
    data = await redis_client.get(key)
    return json.loads(data) if data else None
