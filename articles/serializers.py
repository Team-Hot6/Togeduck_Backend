from rest_framework import serializers
from articles.models import Article, Comment


# 게시글 전체 보기
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    comment_article = serializers.SerializerMethodField()
    cur_time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    def get_cur_time(self, obj):
        ampm = obj.created_at.strftime('%p')
        time = obj.created_at.strftime('%I:%M')
        time = f'AM {time}' if ampm == 'AM' else f'PM {time}'

        # 17번째 줄이랑 같음
        # if ampm == 'AM':
        #     created_time = f'AM {created_time}'
        # else:
        #     created_time = f'MP {created_time}'
        return time
    
    def get_date(self, obj):
        return obj.created_at.strftime('%Y년 %m월 %d일 %A')

    def get_comment_article(self,obj):
        return obj.comment_article.count()

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
        fields = "__all__"
        # exclude = ('updated_at','article',)

# 게시글 상세
class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    # comment_article = CommentListSerializer(many=True)

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"

# 댓글 작성
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)