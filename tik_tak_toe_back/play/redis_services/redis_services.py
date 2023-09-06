from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from play.redis_services.redis_connector import get_redis_connection


async def start_turn_timer(game_id, player, timeout=60):
    redis = await get_redis_connection()
    expiration = (datetime.now() + timedelta(seconds=timeout)).timestamp()
    redis.set(f"turn_timer:{game_id}:{player.pk}", expiration)
    redis.close()


async def get_next_player(game_id, players: list):
    redis = await get_redis_connection()
    User = get_user_model()
    bite_pk_user = redis.get(f"current_turn:{game_id}")
    current_turn = await User.objects.aget(pk=int(bite_pk_user)) if bite_pk_user is not None else None
    if not current_turn:
        current_turn = players[0]
    else:
        current_turn_index = players.index(current_turn)
        next_turn_index = (current_turn_index + 1) % len(players)
        current_turn = players[next_turn_index]
    redis.set(f"current_turn:{game_id}", current_turn.pk)
    redis.close()
    return current_turn


async def get_currently_tur(game_id):
    redis = await get_redis_connection()
    User = get_user_model()
    bite_pk_user = redis.get(f"current_turn:{game_id}")
    return await User.objects.aget(pk=int(bite_pk_user)) if bite_pk_user is not None else None


async def get_remaining_time(game_id, player):
    redis = await get_redis_connection()
    expiration = redis.get(f"turn_timer:{game_id}:{player.pk}")
    redis.close()
    if expiration:
        expiration_timestamp = float(expiration)
        current_timestamp = datetime.now().timestamp()
        remaining_time = max(0, int(expiration_timestamp) - int(current_timestamp))
        return remaining_time

    return 0.0


async def clear_data(game_id, players):
    redis = await get_redis_connection()
    for player in players:
        if redis.get(f"turn_timer:{game_id}:{player.pk}"):
            redis.delete(f"turn_timer:{game_id}:{player.pk}")
    if redis.get(f"current_turn:{game_id}"):
        redis.delete(f"current_turn:{game_id}")
