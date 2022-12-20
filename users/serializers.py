from articles.models import Article
from users.models import User
from rest_framework import serializers
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from workshops.serializers import HobbySerializer, WorkshopSerializer, WorkshopApplySerializer, MypageWorkshopLikeSerializer
from workshops.models import Workshop



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
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email":"이메일 중복됐습니다."})

        if User.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})

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
        token['nickname'] = user.nickname  

        # 채팅에서 쓸 user id 저장해줌
        token['user_id'] = user.id
        token['nickname'] = user.nickname
        return token

# user list view serializer
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)




class MypageSerializer(serializers.ModelSerializer): # 마이페이지 - 전체적인 정보 불러오기
    workshop_likes = MypageWorkshopLikeSerializer(many=True)
    hobby = HobbySerializer(many=True)
    workshop_host = WorkshopSerializer(many=True)
    workshop_apply_guest = WorkshopApplySerializer(many=True)
    class Meta:
        model = User
        fields = ('nickname', 'email', 'profile_image', 'workshop_likes', 'hobby', 'workshop_host', 'workshop_apply_guest')


# 비밀번호 변경
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True) # 새로운 비번, 비번 유효성 검사
    password2 = serializers.CharField(write_only=True, required=True) # 새로운 비번 확인
    old_password = serializers.CharField(write_only=True, required=True) # 현재 비번
    

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in attrs["password"])

        if attrs['password'] == attrs['old_password']:
            raise serializers.ValidationError({"password": " 현재 사용중인 비밀번호와 동일한 비밀번호를 사용할 수 없습니다 "})

        if len(attrs["password"]) < 2 or password:
            raise serializers.ValidationError({"password":"password는  2자 이상 특수문자 포함 "})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 동일하지 않습니다 "})

        return attrs

    def validate_old_password(self, value): # 현재 비번 확인 
        user = self.context['request'].user # 로그인한 유저 정보 가져오기
        if not user.check_password(value): # 로그인한 유저의 비번이 아니라면
            raise serializers.ValidationError({"old_password": "기존 비밀번호를 똑바로 입력하세요"})
        return value

    def update(self, instance, validated_data): # 새로운 비번 저장

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


# 마이페이지 정보 변경(닉네임, 이메일, 프로필 사진)
class MypageInfoPutSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ('profile_image', 'nickname', 'email',)

    def validate(self, data):

        email = data["email"]
        email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password = all(x not in ["!", "@", "#", "$", "%", "^", "&", "*", "_"] for x in data["password"])
        if not email_validation.fullmatch(email) :
            raise serializers.ValidationError({"email":"이메일 형식을 확인해주세요"})

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email":"이메일 중복됐습니다."})

        if User.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError({"nickname":"중복된 닉네임이 있습니다."})
        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError({"nickname":"nickname을 두 글자 이상 작성해주세요."})

        return data