from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from articles import serializers
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   # jwt 토큰 커스터마이징 사용자 인증
)
from rest_framework import permissions # 사용자 권한
from rest_framework.generics import get_object_or_404
from users.models import User

# Create your views here.

# 회원가입
class UserView(APIView):
    def post(self, request):
        print('꺄아아아아아ㅏ앙ㄱ')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print('유효성검사 통과해줘',serializer)
            serializer.save()
            return Response({"message":"가입완료 ㅇㅅㅇ"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# jwt 토큰 커스터마이징 
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer # 시리얼라이저 jwt 커스텀모델