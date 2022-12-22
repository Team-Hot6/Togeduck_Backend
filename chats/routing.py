from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    # path('ws/socket-server/<int:room_id>/', consumers.CreateRoom.as_asgi()),
    re_path(r"^ws/socket-server/(?P<room_id>[^/]+)/$", consumers.CreateRoom.as_asgi()),
]