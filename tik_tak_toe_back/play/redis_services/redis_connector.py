import redis


async def get_redis_connection():
    redis_ = redis.from_url('redis://localhost')
    return redis_

