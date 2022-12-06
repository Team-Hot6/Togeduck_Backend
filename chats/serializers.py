from rest_framework import serializers
from chats.models import ChatRoom, RoomMessage
from users.models import User


class ChatRoomSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.nickname

    class Meta:
        model = ChatRoom
        fields = '__all__'

class RoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessage
        fields = '__all__'