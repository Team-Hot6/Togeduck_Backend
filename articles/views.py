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
from django.db.models import Count
# test
from .articlecron import get_score
from django.db.models import Count
from datetime import datetime
from django.db import transaction


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
                self.queryset = Article.objects.annotate(like_count=Count('like').order_by('-like_count', '-created_at'))

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

        query_list = []
        for idx in lank_list:
            try:
                obj = Article.objects.get(id=idx)
                query_list.append(obj)
            except:
                continue

        if not query_list:
            obj = Article.objects.annotate(like_count=Count('like')).order_by('-like_count', '-created_at')[0:10]
            slz = ArticleListSerializer(obj, many=True)
            return Response(slz.data, status=status.HTTP_200_OK)
            
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
        # 당일날 밤 12시에 쿠키 초기화
        tomorrow = datetime.replace(datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        serializer = ArticleDetailSerializer(article)
        
        response = Response(serializer.data, status=status.HTTP_200_OK)

        print(request.COOKIES)
        # 쿠키 읽기 & 생성
        if request.COOKIES.get('hit'):
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|')
            if str(article_id) not in cookies_list:
                response.set_cookie('hit', cookies+f'|{article_id}', expires=expires) # 쿠키 생성
                with transaction.atomic(): # 모델 필드인 views에 1 추가
                    article.views += 1
                    article.save()
        else:
            response.set_cookie('hit', article_id, expires=expires)
            article.views += 1
            article.save()
        
        return response
    
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
        cookie = request.COOKIES
        print(cookie)

        if 'testcookie' in cookie:
            return Response('성공!')

        response = Response('cookie')
        response.set_cookie('testcookie', 'testtest')
        return response
