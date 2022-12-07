from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoomMessage, ChatRoom
from django.db.models import Q
from .serializers import ChatRoomSerializer, RoomMessageSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserListSerializer
from itertools import chain
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
    def post(self, request):
        sender_id = request.user.id
        receiver_id = request.data['user_id']

        sender = request.user
        receiver = User.objects.get(id=receiver_id)

        # 서로의 채팅방이 있는지 확인 함
        get_exist_room = ChatRoom.objects.filter(
            Q(sender=sender_id, receiver=receiver_id) | Q(sender=receiver_id, receiver=sender_id))

        # 채팅룸이 없으면 생성해서 반환해줌
        if not get_exist_room:
            new_room = ChatRoom.objects.create(sender=sender, receiver=receiver)
            return Response(new_room.id, status=status.HTTP_200_OK)
        
        # 존재하는 채팅방 id 반환
        return Response(get_exist_room[0].id, status=status.HTTP_200_OK)

# 개별 채팅방 관리
class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 채팅방이 있는지 확인하고 없으면 없다고 리턴
    # 채팅방이 존재하면 존재하는 채팅방 데이터 리턴
    # 채팅방 접속 하자마자 채팅 읽음 상태 만드는 로직 작성 예정
    def get(self, request, room_id):
        try:
            check_chat_room = ChatRoom.objects.get(id=room_id)
        except:
            return Response({"msg":"채팅방이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 채팅방 접속하면 해당 채팅방 읽음 처리
        check_chat_room.is_read = True
        check_chat_room.save()
        slz = RoomMessageSerializer(check_chat_room)

        return Response(slz.data, status=status.HTTP_200_OK)
    
    # 실시간으로 읽은 처리 하는 로직 구현 필요
    
    def post(self, request, room_id):
        return Response('', status=status.HTTP_200_OK)

# 최신순으로 정렬하는 로직 추가 예정
class UserListView(APIView):
    def get(self, request):
        connect_user = self.request.GET.get('connect')
        # connect 가 파라미터에 없을때 전체를 반환해줌
        if not connect_user:
            user_list = User.objects.all()
            slz = UserListSerializer(user_list, many=True)

            return Response(slz.data, status=status.HTTP_200_OK)
        
        # 로그인된 유저의 채팅 목록을 반환해줌
        if connect_user == 'list':
            cur_user_id = request.user.id
            user_chat_rooms = ChatRoom.objects.filter(
                Q(sender=cur_user_id) | Q(receiver=cur_user_id))
            
            # sender로 있는 채팅 상대방 객체
            
            opponent_receiver = ChatRoom.objects.filter(sender=cur_user_id)
            opponent_sender = ChatRoom.objects.filter(receiver=cur_user_id)

            test_user = User.objects.get(id=cur_user_id)

            # 되는거 related name 사용
            # ex ) (객체).(related_name).all()
            test2 = test_user.chatroom_sender.all()

            # 되는거 related name 없이 _set 사용
            # ex) (객체).(모델_set).all() # 대소문자 구분 없음
            # test2 = test_user.chatroom_set.all()

            set_opponent_receiver = User.objects.filter(id=cur_user_id)
            temp_set_opp_receiver = [x.chatroom_receiver.all() for x in set_opponent_receiver]

            # print(set_opponent_receiver)
            # print(temp_set_opp_receiver)

            temp_opp_receiver = [User.objects.get(email=x.receiver) for x in opponent_receiver]
            temp_opp_sender = [User.objects.get(email=x.sender) for x in opponent_sender]

            # https://stackoverflow.com/questions/431628/how-can-i-combine-two-or-more-querysets-in-a-django-view
            result_opp_user = list(chain(temp_opp_receiver, temp_opp_sender))

            slz = UserListSerializer(result_opp_user, many=True)
            
            # 테스트 정렬 코드

            room_list = ChatRoom.objects.filter(Q(sender=cur_user_id)|Q(receiver=cur_user_id))
            print(room_list)
            print(room_list)

            # message_list = RoomMessage.objects.filter(room__in=room_list.values('id', flat=True)).order_by('created_at')

            # gt lt

            # print(message_list)

            # message_dict = {}

            # for message in message_list:
            #     message_dict[message.room] = message
            
            
            
            return Response(slz.data, status=status.HTTP_200_OK)
        
        return Response({"msg" : "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
    
"""
room_list = ChatRoom.objects.filter(Q(sender=user)|Q(receiver=user))
room_info_list = []
for room in room_list:
room_info_list.append({
'room_id': room.id,
'receiver': room.receiver,
'sender': room.sender,
'last_message': None
})


room_id_list = list(room_list.values('id', flat=True))
message_list = RoomMessage.objects.filter(room__in=room_id_list).order_by('created_at')

message_dict = {}

for message in message_list:
message_dict[message.room.id] = message

for room in room_info_list:
room['last_message'] = message_dict[room.id]

room_info_list = sorted(
room_info_list,
key=lambda item: item['last_massage'].created_at
reverse=True
)
"""