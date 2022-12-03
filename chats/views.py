from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoomMessage, ChatRoom
from django.db.models import Q
from .serializers import ChatRoomSerializer, RoomMessageSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    # 채팅방 목록 가져오기 로그인 필요
    def get(self, request):
        user = request.user
        user_chatroom_list = ChatRoom.objects.filter(Q(sender=user.id) | Q(receiver=user.id))
        slz = ChatRoomSerializer(user_chatroom_list, many=True)

        return Response(slz.data, status=status.HTTP_200_OK)
    
    # 채팅방 생성하기
    def post(self, request, user_id):
        sender = request.user.id
        receiver = user_id
        
        return Response('', status=status.HTTP_200_OK)