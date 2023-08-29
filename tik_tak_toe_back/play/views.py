from adrf.decorators import api_view
from rest_framework.response import Response
from play.redis_services.redis_services import get_remaining_time


@api_view(['GET'])
async def get_timer_turn(request):
    if request.method == 'GET':
        play_hash_code = request.query_params.get('play_hash_code')
        player_id = request.query_params.get('player_id')
        is_expired = await get_remaining_time(play_hash_code, player_id)
        return Response({"remaining_time": is_expired})
