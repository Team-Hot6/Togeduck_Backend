from django.contrib import admin
from .models import ChatRoom, RoomMessage

admin.site.register(ChatRoom)
admin.site.register(RoomMessage)
