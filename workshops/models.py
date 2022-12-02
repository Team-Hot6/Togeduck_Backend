from django.db import models
from users.models import User


# Create your models here.

class Hobby(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return self.category 

class Location(models.Model):
    district = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

class Workshop(models.Model):
    category = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_host')
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    workshop_image = models.ImageField(upload_to='media/workshop/')
    max_client = models.IntegerField()
    amount = models.DecimalField(decimal_places=0, max_digits=10000000000000000)
    created_at = models.DateTimeField(auto_now_add=True)
    participant = models.ManyToManyField(User, related_name='member', symmetrical=False)
    likes = models.ManyToManyField(User, related_name='workshop_likes')
    








