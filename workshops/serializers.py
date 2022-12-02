from rest_framework import serializers
from workshops.models import Review


# 댓글 보기 GET
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj): 
        return obj.user.email 

    class Meta:
        model = Review 
        fields = '__all__' 
       




# 댓글 작성 POST
# 댓글 수정 PUT 
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content',) 




