from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer, MypageInfoPutSerializer
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

import requests
# STEP 2 : 전달 받은 코드 값과 함께 카카오 서버에 토큰 요청
class KakaoCallBackView(APIView):
    def get(self, request):
        code = request.GET.get('code')
        print('전달받은 코드 값 : ', code)
        
        if not code:
            error = request.GET.get('error')
            print("에러 정보 확인 테스트: " ,error)
            error_description = request.GET.get('error_description')
            return Response({"message": error_description}, status=status.HTTP_400_BAD_REQUEST)
        
        rest_api_key = "aea6c7b586cd433bf7056d8ab7cd1862",
        redirect_uri = "http://127.0.0.1:8000/users/kakao/callback/"

        data = {
            "grant_type": "authorization_code",
            "client_id": rest_api_key,
            "redirect_uri": redirect_uri,
            "code": code,
        }

        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        
        # 문제 : 전달 받은 코드와 필수 파라미터 값을 카카오 서버에 post 요청 보내야 하는데 TypeError: 'QueryDict' object is not callable 에러 발생!
        # 원인 : request는 dictioinoary type(QueryDict)으로 변환하는데 key 값을 가진 key가 존재하면 해당 key에 대한 값을 반환하고, 존재하지 않을 경우 KeyError가 발생(요청 보낼 주소는 dict 타입이 아님)
        # 해결방법 : python의 requests 모듈을 사용하여 post 요청하는 방법
        request_token = requests.post(kakao_token_api, data=data).json()

        # STEP 3 : 코드를 사용하여 전달받은 토큰을 헤더에 실어 아래 kakao_user_api로 GET 요청하여 토큰에 담긴 사용자 정보 가져온다. 
        kakao_access_token = request_token['access_token']
        kakao_refresh_token = request_token['refresh_token']
        
        print("카카오 엑세스 토큰 : " , kakao_access_token)
        print("카카오 리프레쉬 토큰 : " , kakao_refresh_token)
        
        kakao_user_api = 'https://kapi.kakao.com/v2/user/me'
        header = {"Authorization": f"Bearer ${kakao_access_token}"}
        user_info = requests.get(kakao_user_api, headers=header).json()

        # 유저 정보 response ex)
        # {'id': 2588628171, 'connected_at': '2022-12-21T00:12:25Z', 
        # 'properties': {'nickname': '규현', 'profile_image': 'http://k.kakaocdn.net/dn/bBDjw3/btrJSLREbyo/klPh6YQud6Exb8OYGB1Jr0/img_640x640.jpg', 'thumbnail_image': 'http://k.kakaocdn.net/dn/bBDjw3/btrJSLREbyo/klPh6YQud6Exb8OYGB1Jr0/img_110x110.jpg'}, 
        # 'kakao_account': {'profile_nickname_needs_agreement': False, 'profile_image_needs_agreement': False, 
        # 'profile': {'nickname': '규현', 'thumbnail_image_url': 'http://k.kakaocdn.net/dn/bBDjw3/btrJSLREbyo/klPh6YQud6Exb8OYGB1Jr0/img_110x110.jpg', 'profile_image_url': 'http://k.kakaocdn.net/dn/bBDjw3/btrJSLREbyo/klPh6YQud6Exb8OYGB1Jr0/img_640x640.jpg', 'is_default_image': False},
        # 'has_email': True, 'email_needs_agreement': False, 'is_email_valid': True, 'is_email_verified': True, 'email': 'rlarbgus95@naver.com'}}
        
        user_email_agreement = user_info['kakao_account']['email_needs_agreement']
        # 디버깅용 True
        user_email_agreement = bool(True)
        # 이메일 제공 동의
        if user_email_agreement == True:
            has_email = user_info['kakao_account']['has_email']
            # 이메일 존재 여부
            if has_email == True:
                is_email_valid = user_info['kakao_account']['is_email_valid']
                # 이메일 유효 여부
                if is_email_valid == True:
                    is_email_verified = user_info['kakao_account']['is_email_verified']
                    # 이메일 인증 여부
                    if is_email_verified == True:
                        # 유저 이메일 정보
                        email = user_info['kakao_account']['email']
        
        user_profile_image_agreement = user_info['kakao_account']['profile_image_needs_agreement']
        # 디버깅용 True
        user_profile_image_agreement = bool(True)
        # 프로필 사진 제공 동의
        if user_profile_image_agreement == True:
            # 유저 프로필 정보
            user_profile = user_info['kakao_account']['profile']['profile_image_url']
        # 유저 닉네임 정보
        user_nickname = user_info['kakao_account']['profile']['nickname']

        exist_user = User.objects.filter(nickname=user_nickname)
        
        # 가입된 유저는 로그인
        if exist_user:
            user = User.objects.get(email=email)

            pass
        # 가입되지 않은 유저는 회원가입
        else:
            
            pass
        pass