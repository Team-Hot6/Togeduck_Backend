from django.db import models
from users.models import User

# Create your models here.
class ChatRoom(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Room_sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Room_receiver')

    def __str__(self):
        return str(self.sender)

class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.room)
    