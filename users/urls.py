from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 
from users import views

urlpatterns = [ # jwt
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # access 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refesh
    path('signup/', views.UserView.as_view(), name="UserView"), # 회원가입
    path('<int:user_id>/', views.MypageView.as_view(), name="ProfileView"), # 마이페이지
    path('<int:user_id>/put/', views.MypageInfoPutView.as_view(), name="ProfileView"), # 마이페이지 - 개인정보 수정
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('kakao/callback/', views.KakaoCallBackView.as_view(), name='kakao_callback_view'), # 카카오 콜백 함수
]
