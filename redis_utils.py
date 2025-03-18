import json

import redis.asyncio as redis

redis_client: redis.Redis = None


async def redis_init():
    """
    Initialize Redis connection
    """
    global redis_client
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def redis_close():
    """
    Close Redis connection
    """
    global redis_client
    await redis_client.close()


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
