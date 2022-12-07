from django.db import models
from users.models import User

# Create your models here.
class ChatRoom(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chatroom_sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chatroom_receiver')

    def __str__(self):
        return str(f'id : {self.id}, sender : {self.sender}, receiver : {self.receiver}')

class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='roommessage_room')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.room)
    