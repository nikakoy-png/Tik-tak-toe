from adrf.decorators import api_view
from rest_framework.response import Response

from play.Factory.creator_play_setting import CreatePlay
from play.Factory.play_creator import PlayCreator
from play.redis_services.redis_services import is_turn_expired


@api_view(['GET'])
async def get_timer_turn(request):
    player = request.user
    play_hash_code = request.query_params.get('play_hash_code')
    is_expired = await is_turn_expired(play_hash_code, player)
    return Response({"is_turn_expired": is_expired})
