from rest_framework import serializers
from users.models import User # 모델
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # jwt 토큰 커스터마이징
import re




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
        
            raise serializers.ValidationError("이메일 형식 틀림ㅋㅋ")
        

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("이메일 중복 있음ㅋㅋㅋ")


        if User.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError(detail={"error":"중복 닉네임 있는데요?ㅋㅋ"})

        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError("nickname은 2자 이상임 ")
                          

        elif len(data["password"]) < 2 and password:
            raise serializers.ValidationError("비밀번호는 2자 이상 특수문자 포함해")

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

    
    

# jwt 토큰 커스텀 이메일 추가 (임포트한 토큰시리얼라이저)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email # 이메일로 바꿈/추가
        token['nickname'] = user.nickname
        return token