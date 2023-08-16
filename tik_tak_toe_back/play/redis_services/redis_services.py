from datetime import datetime, timedelta

from django.contrib.auth import get_user_model

from play.redis_services.redis_connector import get_redis_connection

User = get_user_model()


async def start_turn_timer(game_id, player_id, timeout=60):
    redis = await get_redis_connection()
    expiration = (datetime.now() + timedelta(seconds=timeout)).timestamp()
    await redis.set(f"turn_timer:{game_id}:{player_id}", expiration)
    redis.close()
    await redis.wait_closed()


async def get_next_player(game_id, players) -> User:
    redis = await get_redis_connection()
    current_turn = await redis.get(f"current_turn:{game_id}")
    if not current_turn:
        current_turn = players[0]
    else:
        current_turn_index = players.index(current_turn)
        next_turn_index = (current_turn_index + 1) % len(players)
        current_turn = players[next_turn_index]
    await redis.set(f"current_turn:{game_id}", current_turn)
    redis.close()
    await redis.wait_closed()
    return current_turn


async def is_turn_expired(game_id, player_id):
    redis = await get_redis_connection()
    expiration = await redis.get(f"turn_timer:{game_id}:{player_id}")
    redis.close()
    await redis.wait_closed()
    if expiration:
        return float(expiration) < datetime.now().timestamp()
    return False
