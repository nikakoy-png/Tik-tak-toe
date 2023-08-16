import hashlib
import datetime
from django.db import IntegrityError
from play.Factory.creator_play_setting import CreatePlay
from play.Factory.play_creator import PlayCreator


async def create_play(users, play_type):
    data_hash_code = users[0][0].username + users[-1][0].username + str(datetime.datetime.now())
    play_hash_code = hashlib.sha256(data_hash_code.encode('utf-8')).hexdigest()
    try:
        model = await CreatePlay(PlayCreator(), play_type)
        await model.objects.acreate(play_hash_code=play_hash_code,
                                    user1=users[0][0],
                                    user2=users[-1][0])
    except IntegrityError:
        return None
    return play_hash_code
