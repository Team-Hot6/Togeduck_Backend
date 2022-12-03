from rest_framework import serializers
from workshops.models import Hobby, Location, Workshop, Review


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer): # 특정 워크샵 상세조회에 사용되는 리뷰
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = ('id', 'content', 'user', 'created_at', 'updated_at',)


class WorkshopListSerializer(serializers.ModelSerializer): # 워크샵 전체 목록 조회
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.category

    def get_location(self, obj):
        return obj.location.district

    class Meta:
        model = Workshop
        fields = ('title', 'content', 'workshop_image', 'category', 'location',)


class WorkshopSerializer(serializers.ModelSerializer): # 특정 워크샵 상세 조회
    host = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    review_workshop = ReviewSerializer(many=True)

    def get_host(self, obj):
        return obj.host.nickname

    def get_category(self, obj):
        return obj.category.category

    def get_location(self, obj):
        return obj.location.district
  
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_participant_count(self, obj):
        return obj.participant.count()

    class Meta:
        model = Workshop
        fields = ('title', 'content', 'workshop_image', 'category', 'location', 'address', 'host', 'amount', 'date', 'created_at', 'max_client', 'participant_count', 'likes_count', 'review_workshop',)


class WorkshopCreateSerializer(serializers.ModelSerializer): # 워크샵 생성
    class Meta:
        model = Workshop
        fields = ('title', 'content', 'workshop_image', 'category', 'location', 'address', 'amount', 'date', 'max_client',)