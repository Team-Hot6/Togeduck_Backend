from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer,UserProfileSerializer,UserProfileHobbySerializer,UserProfileparticipantSerializer,UserProfileWorkshopSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
from rest_framework.generics import get_object_or_404
from users.models import User


# Create your views here.

# 회원가입
class UserView(APIView):
    def post(self, request):
        print('나와라라라라라랄',request.data)
        serializer = UserSerializer(data=request.data)
        print('여기까지 찍히나나난')
        if serializer.is_valid(raise_exception=True):
            print('흐어어어어엉')
          
            serializer.save()
            return Response({"message":"가입완료 ㅇㅅㅇ"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 로그인 토큰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 



# 프로필페이지
class ProfileView(APIView):
    def get(self, request, user_id):

        user = get_object_or_404(User,id=user_id) 
        if request.user == user: 
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('접근권한이 없습니다', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,user_id ): 
        profile = get_object_or_404(User,id=user_id) 
        if request.user == profile: 
            serializer = UserProfileSerializer(profile, data=request.data) 

            
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        else:
            return Response('접근권한이 없습니다', status=status.HTTP_400_BAD_REQUEST)

# 프로필 취미
class ProfileHobbyView(APIView):
    def get(self, request, user_id):

        user = get_object_or_404(User,id=user_id) 
        if request.user == user: 
            serializer = UserProfileHobbySerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('접근권한이 없습니다', status=status.HTTP_400_BAD_REQUEST)

# 프로필 신청한 워크샵
class ProfileparticipantView(APIView):
    def get(self, request, user_id):

        user = get_object_or_404(User,id=user_id) 
        if request.user == user: 
            serializer = UserProfileparticipantSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('접근권한이 없습니다', status=status.HTTP_400_BAD_REQUEST)

# 프로필 생성한 워크샵
class ProfileWorkshopView(APIView):
    def get(self, request, user_id):

        user = get_object_or_404(User,id=user_id) 
        if request.user == user: 
            serializer = UserProfileWorkshopSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response('접근권한이 없습니다', status=status.HTTP_400_BAD_REQUEST)