import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        # send message example
        # await self.send(text_data=json.dumps({
        #     'type':'connect hyeong',
        #     'message':'plz suc'
        #     }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # get message receive example
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        print(msg)


class CreateRoom(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]

        await self.accept()
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))