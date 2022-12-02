from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/socket-server/', consumers.ChatConsumer.as_asgi()),
    path('ws/socket-server/<int:room_id>/', consumers.CreateRoom.as_asgi()),
]