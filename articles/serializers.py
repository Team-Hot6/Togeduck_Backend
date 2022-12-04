from rest_framework import serializers
from articles.models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

# 게시글 전체 보기
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    comment_article = serializers.SerializerMethodField()

    def get_comment_article(self,obj):
        return obj.comment_article.count()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"

# 게시글 상세
class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    comment_article = serializers.StringRelatedField(many=True, read_only=True)

    def get_comment_article(self, obj):
        return obj.comment_article.content

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"

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
        fields = ('content', 'created_at', 'user')