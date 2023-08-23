import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from play.routing import websocket_urlpatterns
from tik_tak_toe_back.authentication import WebSocketTokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tik_tak_toe_back.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            WebSocketTokenAuthMiddleware(
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
            )
        ),
    }
)