from django.db import models
from users.models import User


class Hobby(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.category)

class Location(models.Model):
    district = models.CharField(max_length=20)

    def __str__(self):
        return str(self.district)

class Workshop(models.Model):
    category = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_host')
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    address = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    workshop_image = models.ImageField(upload_to='workshop/')
    max_client = models.IntegerField()
    amount = models.DecimalField(decimal_places=0, max_digits=10000000000000000)
    created_at = models.DateTimeField(auto_now_add=True)
    participant = models.ManyToManyField(User, related_name='member', symmetrical=False, blank=True)
    likes = models.ManyToManyField(User, related_name='workshop_likes', blank=True)

    def __str__(self):
        return str(self.title)