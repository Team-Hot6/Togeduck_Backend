from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoomMessage, ChatRoom
from django.db.models import Q
from .serializers import ChatRoomSerializer, RoomMessageSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# user의 채팅방 목록 가져오기
class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_chatroom_list = ChatRoom.objects.filter(Q(sender=user.id) and Q(receiver=user.id))
        slz = ChatRoomSerializer(user_chatroom_list,)

        return Response(request.data, status=status.HTTP_200_OK)