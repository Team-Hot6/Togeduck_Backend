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

# 게시글 생성
class ArticleCreateView(APIView):
    # 게시글 작성
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"msg":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serialzier = ArticleSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save(user=request.user)
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)