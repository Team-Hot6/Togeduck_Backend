import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import ChatRoom, RoomMessage
from users.models import User
from channels.db import database_sync_to_async
from datetime import datetime

# test code
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 로그인된 사용자인지 확인
        # 추 후 토큰인증 확인 코드 추가
        if self.scope['user']:
            pass
        else:
            self.close()
        await self.accept()
                
    # get message receive example
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        room_id = text_data_json['room_id']
        message = text_data_json['message']
        # 프론트에서 sender_id, receiver_id 보내주는 로직 필요
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        
        sender = await self.get_user_db(sender_id)
        receiver = await self.get_user_db(receiver_id)
        room_object = await self.get_chatroom_db(room_id)

        if not sender:
            print('Sender user가 조회되지 않습니다.')
        if not receiver:
            print('Receiver user가 조회되지 않습니다.')
        
        await self.create_chat_log(room_object, sender, message)

        cur_datetime = datetime.now()
        ampm = cur_datetime.strftime('%p')

        cur_time = datetime.now().strftime('%I:%M')            
        date = datetime.now().strftime('%Y년 %m월 %d일')
        cur_time = f"AM {cur_time}" if ampm == 'AM' else f"PM {cur_time}"

        response_json = {
            'message': message,
            'sender': sender.id,
            'room_id': room_id,
            'cur_time': cur_time,
            'date': date
            }
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(response_json)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

# get room_id test
class CreateRoom(AsyncWebsocketConsumer):
    # django channels authentication 로그인 관련한 인증 기능 추가해야 함
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room_id = text_data_json['room_id']
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        
        sender = await self.get_user_db(sender_id)
        room_object = await self.get_chatroom_db(room_id)
        user_email = await self.get_user_email(sender_id)

        sender_profile_image = sender.profile_image

        if not sender:
            print('Sender user가 조회되지 않습니다.')
        if not message:
            print('message가 없습니다.')
            return
        
        await self.create_chat_log(room_object, sender, message)

        cur_datetime = datetime.now()
        ampm = cur_datetime.strftime('%p')

        cur_time = datetime.now().strftime('%I:%M')
        date = datetime.now().strftime('%Y년 %m월 %d일')
        cur_time = f"AM {cur_time}" if ampm == 'AM' else f"PM {cur_time}"

        response_json = {
            'message': message,
            'sender': sender.id,
            'room_id': room_id,
            'cur_time': cur_time,
            'date': date,
            'user': user_email,
            'profile_image': f'{sender_profile_image}'
            }
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(response_json)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message_data = json.loads(event['message'])
        message = message_data['message']
        sender = message_data['sender']
        cur_time = message_data['cur_time']
        date = message_data['date']
        room_id = message_data['room_id']
        user = message_data['user']
        profile_image = message_data['profile_image']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender,
            "cur_time": cur_time,
            "date": date,
            "room_id": room_id,
            'user': user,
            'profile_image': profile_image
            }))

    @database_sync_to_async
    def get_user_db(self, user_id):
        user = User.objects.filter(id=user_id)
        if user:
            return user[0]
        return None
    
    @database_sync_to_async
    def get_chatroom_db(self, room_id):
        room = ChatRoom.objects.filter(id=room_id)
        if room:
            return room[0]
        return None
    
    @database_sync_to_async
    def get_user_email(self, user_id):
        user = User.objects.filter(id=user_id)
        if user:
            return user[0].email
        return None
    
    @database_sync_to_async
    def create_chat_log(self, room_object, sender, content):
        RoomMessage.objects.create(room=room_object, user=sender, content=content)