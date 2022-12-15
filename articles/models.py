from django.db import models
from users.models import User
from workshops.models import Hobby
from .utils import rename_imagefile_to_uuid


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_user')
    category = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='article_category')
    title = models.CharField(max_length=500)
    content = models.TextField()
    article_image = models.ImageField(upload_to=rename_imagefile_to_uuid, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, blank=True, related_name='article_like')
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_article')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
