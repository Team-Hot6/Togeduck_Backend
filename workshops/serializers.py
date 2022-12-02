from workshops.models import Workshop
from rest_framework import serializers


# 마이페이지

class WorkshopMypageSerializer(serializers.ModelSerializer): # 마이페이지 - 내가 선택한 취미, 신청 워크샵, 생성 워크샵
    class Meta:
        model = Workshop
        fields = ("category", "title", "date", "likes" ,"apply_status", "participant", "max_client")


class WorkshopDetailSerializer(serializers.ModelSerializer): # 워크샵 상세 페이지
    likes_count = serializers.SerializerMethodField()
    def get_likes_count(self, obj):
        return obj.likes.count()
    class Meta:
        model = Workshop
        fields = ("workshop_image", "likes", "likes_count", "content", "max_client", "amount", "date", "location")


class WorkshopDetailLikesSerializer(serializers.ModelSerializer):  # 워크샵 상세 페이지 - 좋아요 수정 
    class Meta: 
        model = Workshop
        fields = ("likes")


class WorkshopDetailImageSerializer(serializers.ModelSerializer):  # 워크샵 상세 페이지 - 이미지 수정 
    class Meta: 
        model = Workshop
        fields = ("workshop_image")


