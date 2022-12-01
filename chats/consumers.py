import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from time import sleep

class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.accept()
        
        sleep(1)
        self.send(text_data=json.dumps({
            'type':'connect hyeong',
            'message':'plz suc'
            }))