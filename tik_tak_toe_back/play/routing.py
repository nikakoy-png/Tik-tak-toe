from django.urls import re_path
from play import consumers

websocket_urlpatterns = [
    re_path(r"ws/search-play/(?P<type_play>\w+)/$", consumers.SearchPlay.as_asgi()),
    re_path(r"ws/play/(?P<play_type>\w+)/(?P<play_hash_code>\w+)/$", consumers.PlayConsumer.as_asgi())
]
