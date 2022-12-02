from django.db import models
from users.models import User
from workshops.models import Hobby, Workshop

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_user')
    category = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='article_category')
    title = models.CharField(max_length=500)
    content = models.TextField()
    article_image = models.ImageField(upload_to='media/article/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reveiw_user')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='review_workshop')
    content = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
