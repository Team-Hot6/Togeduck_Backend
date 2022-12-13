from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RoomMessage, ChatRoom
from django.db.models import Q
from .serializers import ChatLogSerializer, RoomMessageSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import UserListSerializer
from itertools import chain
# Create your views here.

class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    # 채팅방 목록 가져오기 로그인 필요
    def get(self, request):
        # 안씀
        # user = request.user
        # # 사용자가 참여하고 있는 모든 채팅방을 가져옴
        # user_chatroom_query = ChatRoom.objects.filter(Q(sender=user.id) | Q(receiver=user.id))

        # slz = ChatLogSerializer(user_chatroom_query, many=True)

        # # 마지막 메세지 순으로 정렬하는 로직 추가 예정
        # # solve) serializer에서 RoomMessages 에 마지막 메세지를 기준으로 정렬해보기
        # # sorted_room = sorted(slz.data, key=lambda x: x['created_at'], reverse=True)

        return Response('', status=status.HTTP_200_OK)
    
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
class ChatRoomLogView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 채팅방이 있는지 확인하고 없으면 없다고 리턴
    # 채팅방이 존재하면 존재하는 채팅방 데이터 리턴
    # 채팅방 접속 하자마자 채팅 읽음 상태 만드는 로직 작성 예정
    def get(self, request, room_id):
        try:
            check_chat_room = ChatRoom.objects.get(id=room_id)
        except:
            return Response({"msg":"채팅방이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        is_chat_read = RoomMessage.objects.filter(
            ~Q(user=request.user.id) & Q(room=check_chat_room))

        # 메세지 읽음 처리
        # for read in is_chat_read:
        #     read.is_read = True
        #     read.save()

        # 채팅 로그 반환
        slz = ChatLogSerializer(check_chat_room)

        return Response(slz.data, status=status.HTTP_200_OK)
    
    # 실시간으로 읽은 처리 하는 로직 구현 필요
    
    def post(self, request, room_id):
        return Response('', status=status.HTTP_200_OK)

# 로그인된 사용자와 채팅하고 있는 사용자 가져오기
# 파라미터 없으면 전체 사용자 - 모두
# ?connect=list -> 채팅중인 상대 목록 정렬 X
# ?connect=sort -> 채팅중인 상대 목록 정렬 O
class UserListView(APIView):
    def get(self, request):
        connect_user = self.request.GET.get('connect')
        cur_user_id = request.user.id
        # connect 가 파라미터에 없을때 전체를 반환해줌
        if not connect_user:
            user_list = User.objects.all()
            slz = UserListSerializer(user_list, many=True)

            return Response(slz.data, status=status.HTTP_200_OK)
        
        # 로그인된 유저의 채팅 목록을 반환해줌
        if connect_user == 'list':
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

            temp_opp_receiver = [User.objects.get(email=x.receiver) for x in opponent_receiver]
            temp_opp_sender = [User.objects.get(email=x.sender) for x in opponent_sender]

            result_opp_user = list(chain(temp_opp_receiver, temp_opp_sender))

            slz = UserListSerializer(result_opp_user, many=True)
            return Response(slz.data, status=status.HTTP_200_OK)
            
            # 테스트 정렬 코드
        if connect_user == 'sort':
            room_list = ChatRoom.objects.filter(Q(sender=cur_user_id)|Q(receiver=cur_user_id))

            room_id_list = list(room_list.values_list('id', flat=True))

            # 개선 여지가 있음 모든 것 구현 후 다시 생각해보기
            message_list = RoomMessage.objects.filter(room__in=room_id_list).order_by('created_at')

            message_dict = {}

            for message_obj in message_list:
                message_dict[message_obj.room.id] = message_obj.created_at
            
            # user 상대방 방별로 정렬 완료
            sort_message_room_id = [x[0] for x in sorted([(x, y) for x, y in message_dict.items()], key=lambda x: x[1], reverse=True)]

            temp = []
            
            for i in sort_message_room_id:
                chatroom_obj = ChatRoom.objects.get(id=i)
                if cur_user_id == chatroom_obj.sender.id:
                    temp.append(User.objects.get(id=chatroom_obj.receiver.id))
                else:
                    temp.append(User.objects.get(id=chatroom_obj.sender.id))
            
            slz = UserListSerializer(temp, many=True)
            return Response(slz.data, status=status.HTTP_200_OK)
        
        return Response({"msg" : "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)