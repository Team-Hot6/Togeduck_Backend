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
        # 사용자가 참여하고 있는 모든 채팅방을 가져옴
        user_chatroom_query = ChatRoom.objects.filter(Q(sender=user.id) | Q(receiver=user.id))
        slz = ChatRoomSerializer(user_chatroom_query, many=True)

        # 마지막 메세지 순으로 정렬하는 로직 추가 예정
        # solve) serializer에서 RoomMessages 에 마지막 메세지를 기준으로 정렬해보기
        # sorted_room = sorted(slz.data, key=lambda x: x['created_at'], reverse=True)

        return Response(slz.data, status=status.HTTP_200_OK)
    
    # 채팅방 생성하기
    def post(self, request, user_id):
        sender = request.user.id
        receiver = user_id

        # 서로의 채팅방이 있는지 확인 함
        get_exist_room = ChatRoom.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))

        # 채팅룸이 없으면 생성해서 반환해줌
        if not get_exist_room:
            # 채팅방 만드는 로직
            new_room = ChatRoom.objects.create(sender=sender, receiver=receiver)
            print('##########')
            print(new_room)

            return Response(new_room.id, status=status.HTTP_200_OK)
        
        return Response(get_exist_room[0].id, status=status.HTTP_200_OK)