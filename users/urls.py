from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 
from users import views



urlpatterns = [ 
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # access 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refesh
    path('signup/', views.UserView.as_view(), name="UserView"), # 회원가입
    path('<int:user_id>/', views.ProfileView.as_view(), name='ProfileView'), # 프로필페이지
    path('<int:user_id>/hobby/', views.ProfileHobbyView.as_view(), name='ProfileView'),
    path('<int:user_id>/participant/', views.ProfileparticipantView.as_view(), name='ProfileView'),
    path('<int:user_id>/workshop/', views.ProfileWorkshopView.as_view(), name='ProfileView'),
]
