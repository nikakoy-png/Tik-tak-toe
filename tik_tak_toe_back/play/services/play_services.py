from django.contrib.auth import get_user_model
from play.Factory.creator_play_setting import CreatePlay
from play.Factory.play_creator import PlayCreator

User = get_user_model()


async def is_player_in_game(user: User, play_hash_code: str, type_play: str) -> bool:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.aget(play_hash_code=play_hash_code)
    return True if (play.user1 == user or play.user2 == user) else False


async def get_user_from_play(play_hash_code: str, type_play: str) -> list:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.aget(play_hash_code=play_hash_code)
    return [play.user1, play.user2]