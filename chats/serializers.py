from rest_framework import serializers
from chats.models import ChatRoom, RoomMessage
from users.models import User

class RoomMessageSerializer(serializers.ModelSerializer):
    cur_time = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    def get_cur_time(self, obj):
        ampm = obj.created_at.strftime('%p')
        time = obj.created_at.strftime('%I:%M')
        time = f'AM {time}' if ampm == 'AM' else f'PM {time}'
        return time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일')
    class Meta:
        model = RoomMessage
        fields = '__all__'

# 채팅 로그 slz
class ChatLogSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    room_message = RoomMessageSerializer(many=True, source='roommessage_room')

    class Meta:
        model = ChatRoom
        fields = '__all__'

