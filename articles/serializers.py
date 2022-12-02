from rest_framework import serializers
from articles.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    model = Article
    fields = "__all__"


