from articles.models import Article
from users.models import User
from rest_framework import serializers
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 





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
        
            raise serializers.ValidationError(detail={"email":"이메일 형식 다시 작성해주세여"})
        

        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(detail={"email":"이메일 중복입니닼ㅋ"})


        if User.objects.filter(nickname=data["nickname"]).exists():
                raise serializers.ValidationError(detail={"nickname":"중복 닉네임 있는데요?ㅋㅋ"})

        
        if len(data["nickname"]) < 2:
            raise serializers.ValidationError(detail={"nickname":"nickname은 2자 이상임 "})
                          

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
      
        return token
