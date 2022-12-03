import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import ChatRoom, RoomMessage
from users.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
                
    # get message receive example
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        print(msg)


# get room_id test
class CreateRoom(AsyncWebsocketConsumer):
    async def connect(self):
        # get room_id value
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
        msg = text_data_json['room_id']
        print(msg)

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": msg}
        )

    @database_sync_to_async
    def get_user_db(self, user_id):
        user = User.objects.get()
    


#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))