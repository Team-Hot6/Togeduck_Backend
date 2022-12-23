from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer, MypageInfoPutSerializer, UserNicknameSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView   
)
from users.serializers import MypageSerializer
#from rest_framework.permissions import IsAuthenticated
from rest_framework import generics # UpdateAPIView 임포트 
from allauth.socialaccount.models import SocialAccount


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
            if serializer.is_valid(raise_exception=True): # 유효성 검사시 에러 메세지 띄우기
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# STEP 2 : 전달 받은 코드 값과 함께 카카오 서버에 토큰 요청
class KakaoCallBackView(APIView):
    def post(self, request):
        user_email = request.data.get("email")
        nickname = request.data.get("nickname")
        profile_image = request.data.get("profile_image")
        try:
            user = User.objects.get(email=user_email)
            social_user = SocialAccount.objects.filter(user=user).first()
            
            # 로그인
            if social_user:
                # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입한 유저일때(구글, 네이버)
                if social_user.provider != "kakao":
                    return Response({"error": "카카오로 가입한 유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
                
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
            
            # 동일한 이메일의 유저가 있지만, social계정이 아닐때 
            if not social_user:
                return Response({"error": "이메일이 존재하지만, 소셜유저가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
            
        except:
            # 기존에 가입된 유저가 없으면 새로 가입
            new_user = User.objects.create(
                nickname=nickname,
                email=user_email,
                profile_image=profile_image,
            )
            #소셜account에도 생성
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="kakao",
            )
            refresh = RefreshToken.for_user(new_user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "회원가입 성공"}, status=status.HTTP_200_OK)


class UserNicknameView(APIView):
    def get(self,request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserNicknameSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)