from rest_framework.views import APIView
from articles.models import Article, Comment
from articles.serializers import ArticleListSerializer, ArticleCreateSerializer, ArticleDetailSerializer, CommentListSerializer, CommentCreateSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from workshops.models import Hobby

# request ex) http://www.naver.com/user/?category=축구/

# 게시글 전체 보기
class ArticleView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        get_category_value = self.request.GET.get('category')
        if get_category_value:
            try:
                get_hobby = Hobby.objects.get(category=get_category_value)
            except:
                return Response({"msg":"카테고리가 존재하지 않습니다."}, status=status.HTTP_200_OK)
            articles = Article.objects.filter(category=get_hobby.id)
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        


# 게시글 작성페이지
class ArticleCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"msg":"로그인이 필요합니다!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serialzier = ArticleCreateSerializer(data=request.data)
        if serialzier.is_valid():
            serialzier.save(user=request.user)
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 상세페이지(조회/수정/삭제)
class ArticleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)

        if request.user.is_authenticated:
            article.watch.add(request.user)

        serializer = ArticleDetailSerializer(article)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):    
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"게시글을 수정할 수 있는 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        
        if article.user == request.user:
            article.delete()
            return Response({"msg":"게시글 삭제 완료!"}, status=status.HTTP_200_OK)
        return Response({"msg":"게시글을 삭제할 수 있는 권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


# 게시글의 댓글(조회/작성)
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comments = article.comment_article.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(article_id=article_id, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글의 댓글 삭제
class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            return Response({"msg":"댓글 삭제 완료!"}, status=status.HTTP_200_OK)
        return Response({"msg":"댓글을 삭제할 권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
