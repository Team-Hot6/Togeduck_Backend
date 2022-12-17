from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
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



# 마이페이지
class MypageView(APIView):
    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        serializer = MypageSerializer(user)
        return Response(serializer.data)


# 비밀번호 변경
class ChangePasswordView(generics.UpdateAPIView): # 업데이트 전용 뷰

    queryset = User.objects.all()
    #permission_classes = (IsAuthenticated,) # 로그인 시에만 접근 가능-> 이미 세팅에 'rest_framework_simplejwt.authentication.JWTAuthentication', 있음
    serializer_class = ChangePasswordSerializer