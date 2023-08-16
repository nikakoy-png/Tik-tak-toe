from django.urls import re_path
from play import consumers

websocket_urlpatterns = [
    re_path(r"ws/search-play/(?P<type_play>\w+)/$", consumers.SearchPlay.as_asgi()),
]
