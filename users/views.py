from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
from workshops.models import Workshop
from users.serializers import SelectedHobbySerializer, AppliedWorkshopSerializer, CreatedWorkshopSerializer, UserProfileSerializer



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



# 마이페이지

class UserProfileView(APIView): # 프로필 부분
    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class SelectedHobbyView(APIView):  # 내가 선택한 취미
    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        serializer = SelectedHobbySerializer(user)
        return Response(serializer.data)

class AppliedWorkshopView(APIView):  # 신청 워크샵
    def get(self, request, user_id):  
        applied_workshop = get_object_or_404(User, id=user_id)
        serializer = AppliedWorkshopSerializer(applied_workshop)
        return Response(serializer.data)

class CreatedWorkshopView(APIView):  # 생성 워크샵
    def get(self, request, user_id):  
        created_workshop = get_object_or_404(User, id=user_id)
        serializer = CreatedWorkshopSerializer(created_workshop)
        return Response(serializer.data)



