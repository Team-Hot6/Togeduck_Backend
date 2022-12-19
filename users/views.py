from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer, MypageInfoPutSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
from users.serializers import MypageSerializer
#from rest_framework.permissions import IsAuthenticated
from rest_framework import generics # UpdateAPIView 임포트 




# 회원가입
class UserView(APIView):
    def post(self, request):
       
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True): # 유효성 검사시 에러 메세지 띄우기
           
          
            serializer.save()
            return Response({"message":"가입완료 ㅇㅅㅇ"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 로그인 토큰
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 




class MypageView(APIView): # 마이페이지 - 전체적인 정보 불러오기

    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        serializer = MypageSerializer(user)
        return Response(serializer.data)


# 비밀번호 변경
class ChangePasswordView(generics.UpdateAPIView): # 업데이트 전용 뷰

    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,) # 로그인 시에만 접근 가능-> 이미 세팅에 'rest_framework_simplejwt.authentication.JWTAuthentication', 있음
    serializer_class = ChangePasswordSerializer


# 마이페이지 정보 변경(닉네임, 이메일, 프로필 사진)
class MypageInfoPutView(APIView):
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = MypageInfoPutSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
