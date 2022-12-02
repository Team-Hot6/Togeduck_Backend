from rest_framework import serializers
from workshops.models import Hobby, Location, Workshop


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