from adrf.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from user.services.user_auth import register_user, auth_user, get_user_by_token, get_user_by_id


@api_view(['POST'])
async def register(request):
    return await register_user(request)


@api_view(['POST', 'GET', 'OPTIONS'])
async def login(request):
    if request.method == 'GET':
        return await get_user_by_token(request)
    elif request.method == 'OPTIONS':
        return Response({'Allow': 'GET, POST'}, status=status.HTTP_200_OK, headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        })
    elif request.method == 'POST':
        return await auth_user(request)


@api_view(['GET'])
async def get_user(request, user_id):
    return await get_user_by_id(user_id)
