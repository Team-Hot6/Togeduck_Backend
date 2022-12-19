from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from workshops.models import Workshop
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, MypageSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
from workshops.serializers import WorkshopSerializer



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




class MypageView(APIView): # 마이페이지 - 전체적인 정보 불러오기

    def get(self, request, user_id):  
        user = get_object_or_404(User, id=user_id)
        serializer = MypageSerializer(user)
        return Response(serializer.data)



        

    

        