from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) # jwt
from users import views

urlpatterns = [ # jwt
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # access 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refesh
    path('signup/', views.UserView.as_view(), name="UserView"), # 회원가입
    path('<int:user_id>/hobby/', views.SelectedHobbyView.as_view(), name='selected_hobby'), # 마이페이지 - 내가 선택한 취미
    path('<int:user_id>/apply/', views.AppliedWorkshopView.as_view(), name='applied_workshop'), # 마이페이지 - 신청 워크샵
    path('<int:user_id>/create/', views.CreatedWorkshopView.as_view(), name='applied_workshop'), # 마이페이지 - 생성 워크샵
]
