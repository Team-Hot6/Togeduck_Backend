from rest_framework import serializers
from workshops.models import Review, Workshop


# 댓글 보기 GET
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj): 
        return obj.user.email 

    class Meta:
        model = Review 
        fields = '__all__' 
       




# 댓글 작성 POST
# 댓글 수정 PUT 
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


class WorkshopSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

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
        fields = ('date', 'address', 'title', 'content', 'workshop_image', 'max_client', 'amount', 'category', 'location', 'host', 'likes_count', 'participant_count',)
        read_only_fields = ('host',)