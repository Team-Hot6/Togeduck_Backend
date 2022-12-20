from rest_framework import serializers
from workshops.models import Hobby, Location, Workshop, Review, WorkshopApply
from users.models import User

       

# 댓글 작성 POST, 댓글 수정 PUT 
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content',) 


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
        fields = ('id','content', 'user', 'created_at', 'updated_at','user_id')


# 리뷰 수정 PUT , 작성 POST
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content',) 



class WorkshopApplySerializer(serializers.ModelSerializer):
    guest_nickname = serializers.SerializerMethodField()
    workshop = serializers.StringRelatedField()

    def get_guest_nickname(self, obj):
        return obj.guest.nickname

    class Meta:
        model = WorkshopApply
        fields = ('id', 'guest', 'guest_nickname', 'workshop', 'result', 'created_at',)

class WorkshopListSerializer(serializers.ModelSerializer): # 워크샵 전체 목록 조회
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    workshop_apply = WorkshopApplySerializer(many=True)
    date = serializers.SerializerMethodField()
    cur_time = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.category

    def get_location(self, obj):
        return obj.location.district

    def get_date(self, obj):
        return obj.date.strftime('%Y년 %m월 %d일 %A')

    def get_cur_time(self, obj):
        ampm = obj.date.strftime('%p')
        time = obj.date.strftime('%I:%M')
        time = f'AM {time}' if ampm == 'AM' else f'PM {time}'
        return time

    class Meta:
        model = Workshop
        fields = ('id','title', 'content', 'workshop_image', 'category', 'location', 'date', 'max_guest', 'workshop_apply', 'cur_time', 'views',)


class WorkshopSerializer(serializers.ModelSerializer): # 특정 워크샵 상세 조회
    host = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    review_workshop = ReviewSerializer(many=True)
    workshop_apply = WorkshopApplySerializer(many=True)

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
        fields = ('pk', 'title', 'content', 'workshop_image', 'category', 'location', 'address', 'host', 'host_id', 'amount', 'date', 'created_at', 'max_guest', 'participant', 'participant_count', 'likes_count', 'review_workshop', 'workshop_apply', 'views',)



class WorkshopCreateSerializer(serializers.ModelSerializer): # 워크샵 생성, 수정
    class Meta:
        model = Workshop
        fields = ('title', 'content', 'workshop_image', 'category', 'location', 'address', 'amount', 'date', 'max_guest',)
        read_only_fields = ('workshop_image',)


class MypageWorkshopLikeSerializer(serializers.ModelSerializer): # 마이페이지 - 좋아요 한 워크샵
    location = serializers.SerializerMethodField()
    def get_location(self, obj):
        return obj.location.district
    class Meta:
        model = Workshop
        fields = ( 'pk', 'title', 'workshop_image', 'location', 'address',)

