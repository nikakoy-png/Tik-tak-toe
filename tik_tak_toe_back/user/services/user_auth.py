from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from user.serializers import UserSerializer, UserLoginSerializer, UserRegistrationSerializer


async def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(access)}


async def get_user_by_token(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        print(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


async def get_user_by_id(user_id):
    try:
        from user.models import User
        user = await User.objects.aget(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


async def auth_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if await sync_to_async(serializer.is_valid)():
        user = serializer.validated_data['user']
        tokens = await get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@database_sync_to_async
def get_order_by_rating():
    from user.models import User
    users = User.objects.order_by('-rating')[:10]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


async def register_user(request):
    print(request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    if await sync_to_async(serializer.is_valid)():
        user = await sync_to_async(serializer.save)()
        tokens = await get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
