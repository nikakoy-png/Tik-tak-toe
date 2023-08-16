import aioredis


async def get_redis_connection():
    redis = await aioredis.from_url('redis://localhost')
    return redis

