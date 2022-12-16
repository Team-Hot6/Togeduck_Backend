from rest_framework.views import APIView
from articles.models import Article, Comment
from articles.serializers import ArticleListSerializer, ArticleCreateSerializer, ArticleDetailSerializer, CommentListSerializer, CommentCreateSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from workshops.models import Hobby
from articles.paginations import article_top10_page, article_total_page
from rest_framework.generics import ListAPIView
import json, os
from pathlib import Path
# test
from .articlecron import get_score
from django.db.models import Count


# 페이지네이션 적용 아티클 뷰
class ArticleView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    
    pagination_class = article_total_page
    serializer_class = ArticleListSerializer
    queryset = Article.objects.all()
    
    def get(self, request):
        get_category_id = self.request.GET.get('category')
        sort = self.request.GET.get('sort')

        # category & sort 둘 다 있는 경우
        if get_category_id and sort:
            if sort == 'latest':
                self.queryset = Article.objects.filter(category=get_category_id).order_by('-created_at')
            elif sort == 'like':
                self.queryset = Article.objects.filter(category=get_category_id).annotate(like_count=Count('like')).order_by('-like_count', '-created_at')
        
        # category만 있는 경우
        if get_category_id and not sort:
            self.queryset = Article.objects.filter(category=get_category_id)
        
        # sort만 있는 경우
        if sort and not get_category_id:
            if sort == 'latest':
                self.queryset = Article.objects.all().order_by('-created_at')
            elif sort == 'like':
                self.queryset = Article.objects.annotate(like_count=Count('like')).order_by('-like_count', '-created_at')

        pages = self.paginate_queryset(self.get_queryset())
        slz = self.get_serializer(pages, many=True)
        return self.get_paginated_response(slz.data)

# 인기 게시글 가져오는 view
class ArticleLankView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        BASE_DIR = Path(__file__).resolve().parent.parent
        lank_file_path = os.path.join(BASE_DIR, 'Lank.json')
        
        with open(lank_file_path, "r") as f:
            result_lanking = json.load(f)
        lank_list = result_lanking['result_article_lank']

        query_list = [Article.objects.get(id=x) for x in lank_list]
        slz = ArticleListSerializer(query_list, many=True)

        return Response(slz.data, status=status.HTTP_200_OK)


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

# 게시글 상세페이지(조회/추천/수정/삭제)
class ArticleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        article.views += 1
        article.save()
        serializer = ArticleDetailSerializer(article)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.like.all():
            article.like.remove(request.user)
            return Response({"msg":"취소"}, status=status.HTTP_200_OK)
        else:
            article.like.add(request.user)
            return Response({"msg":"추천"}, status=status.HTTP_200_OK)

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
        if not request.user.is_authenticated:
            return Response({"msg":"로그인 된 사용자만 댓글을 작성할 수 있습니다!"}, status=status.HTTP_401_UNAUTHORIZED)
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

class TestView(APIView):
    def get(self, request):
        get_score()
        return Response('')
