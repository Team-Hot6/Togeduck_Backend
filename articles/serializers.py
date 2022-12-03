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
    comment = serializers.SerializerMethodField()

    def get_comment(self,obj):
        return obj.comment_article.count()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"

# 게시글 작성
class ArticleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('user', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"