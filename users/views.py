from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)

# Create your views here.

# 회원가입
class UserView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            serializer.save()
            return Response({"message":"가입완료 ㅇㅅㅇ"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 로그인 토큰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 