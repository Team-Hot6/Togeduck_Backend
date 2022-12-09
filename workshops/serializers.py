from rest_framework import serializers
from workshops.models import Review, Workshop,Hobby,Location


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'



# 리뷰 보기GET
class ReviewSerializer(serializers.ModelSerializer): 
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = ('content', 'user', 'created_at', 'updated_at',)


# 리뷰 수정 PUT , 작성 POST
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content',) 




# 워크샵 전체 목록 조회
class WorkshopListSerializer(serializers.ModelSerializer): 
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.category

    def get_location(self, obj):
        return obj.location.district

    class Meta:
        model = Workshop
        fields = ('title', 'content', 'workshop_image', 'category', 'location',)








# 워크샵 상세 조회
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
        fields = ('pk', 'title', 'content', 'workshop_image', 'category', 'location', 'address', 'host', 'host_id', 'amount', 'date', 'created_at', 'max_guest', 'participant_count', 'likes_count', 'review_workshop',)



# 워크샵 생성, 수정
class WorkshopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ('date', 'address', 'title', 'content', 'workshop_image', 'max_guest', 'amount', 'category', 'location', )