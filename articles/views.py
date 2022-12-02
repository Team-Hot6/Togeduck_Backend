from rest_framework.views import APIView
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import status, permissions


# 게시글 전체 보기
class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)