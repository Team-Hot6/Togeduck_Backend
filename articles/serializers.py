from rest_framework import serializers
from articles.models import Article, Comment


# 게시글 전체 보기
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    comment_article = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        return obj.like.count()

    def get_time(self, obj):
        time = obj.created_at.strftime('%H:%M')
        return time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일')

    def get_comment_article(self,obj):
        return obj.comment_article.count()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        exclude = ('created_at',)

# 게시글 작성/수정
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('user', )

# 댓글 전체 보기
class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self,obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields = "__all__"
        # exclude = ('updated_at','article',)

# 게시글 상세
class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        return obj.like.count()
    
    def get_time(self, obj):
        time = obj.created_at.strftime('%H:%M')
        return time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일')
    
    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        exclude = ('created_at',)

# 댓글 작성
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)

class ReplyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'