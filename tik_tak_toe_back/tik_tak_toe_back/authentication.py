import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from channels.middleware import BaseMiddleware

from django.contrib.auth import get_user_model


class WebSocketTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        User = get_user_model()

        try:
            print(123123)
            cookies = dict(scope["headers"]).get(b"cookie", b"").decode("utf-8")
            token = None
            if cookies:
                cookie_items = cookies.split(";")
                for item in cookie_items:
                    if item.strip().startswith("token="):
                        token = item.strip().split("=")[1]
                        break

            if token:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = decoded_token.get("user_id")
                if user_id:
                    user = await self.get_user(user_id, User)  # Передаем модель в функцию
                    scope["user"] = user

        except jwt.exceptions.InvalidTokenError:
            pass

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id, User):  # Получаем модель как аргумент
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
