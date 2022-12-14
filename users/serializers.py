from articles.models import Article
from users.models import User
from rest_framework import serializers
import re
from workshops.serializers import WorkshopListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 





# 특정 유저 프로필페이지
class UserProfileSerializer(serializers.ModelSerializer):
   
    member = serializers.SerializerMethodField() # 신청한 워크샵들 
    workshop_likes_count = serializers.SerializerMethodField() # 내가 좋아요한 워크샵 개수

    def get_workshop_likes_count(self, obj):
         return obj.workshop_likes.count()

    def get_member(self, obj):
        return obj.member.count()


    class Meta:
        model = User
        fields = ("id","workshop_likes_count","email","nickname","member","profile_image")
        read_only_fields = ("email",) # PUT 적용 X

# 프로필 선택한 취미
class UserProfileHobbySerializer(serializers.ModelSerializer):

    hobby= serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ("hobby",)



# 프로필 신청한 워크샵
class UserProfileparticipantSerializer(serializers.ModelSerializer):

    member = WorkshopListSerializer(many=True) # 신청한 워크샵들 

    class Meta:
        model = User
        fields = ("member",)

# 프로필 생성한 워크샵
class UserProfileWorkshopSerializer(serializers.ModelSerializer):

    workshop_host = WorkshopListSerializer(many=True) # 작성한 워크샵들 

    class Meta:
        model = User
        fields = ("workshop_host",)



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

        elif len(data["password"]) < 2 or password:
            raise serializers.ValidationError(detail={"password":"password는  2자 이상 특수문자 포함 "})

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
        # 닉네임
        token['nickname'] = user.nickname
        return token

# user list view serializer
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)

