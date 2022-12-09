from articles.models import Article
from users.models import User
from rest_framework import serializers
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from workshops.serializers import WorkshopSerializer, HobbySerializer, WorkshopListSerializer


# 회원가입
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    nickname = serializers.CharField()
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
       
        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError(detail={"email":"이메일 형식을 확인해주세요"})

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(detail={"email":"이메일 중복됐습니다."})

        if User.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError(detail={"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError(detail={"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 and password:
            raise serializers.ValidationError(detail={"password":"password는  2자 이상 특수문자 포함해주세요. "})

        return data

    def create(self, validated_data):
        user = super().create(validated_data) 
        password = user.password 
        user.set_password(password) 
        user.save() 
        return user
    
    def update(self, instance, validated_data):
        user = super().create(validated_data) 
        password = user.password 
        user.set_password(password) 
        user.save() 
        return user

# jwt 토큰 이메일       
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email 
        # 채팅에서 쓸 user id 저장해줌
        token['user_id'] = user.id
        return token

# user list view serializer
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)


# 마이페이지

class UserProfileSerializer(serializers.ModelSerializer): # 프로필 부분
    workshop_likes = WorkshopSerializer
    class Meta:
        model = User
        fields = ('nickname', 'email', 'profile_image', 'workshop_likes', )


class SelectedHobbySerializer(serializers.ModelSerializer): # 내가 선택한 취미
    hobby = HobbySerializer(many=True)
    class Meta:
        model = User
        fields = ('hobby',)


class AppliedWorkshopSerializer(serializers.ModelSerializer): # 신청 워크샵
    workshop_host = WorkshopListSerializer(many=True)
    class Meta:
        model = User
        fields = ('workshop_host',)


class CreatedWorkshopSerializer(serializers.ModelSerializer): # 생성 워크샵
    workshop_host = WorkshopListSerializer(many=True)
    class Meta:
        model = User
        fields = ('workshop_host',)