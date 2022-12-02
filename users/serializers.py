from workshops.serializers import WorkshopMypageSerializer
from articles.models import Article
from users.models import User
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    workshop_category = WorkshopMypageSerializer
    class Meta:
        model = User
        fields = ("nickname","email","hobby","profile_image","workshop_category")
        
    

