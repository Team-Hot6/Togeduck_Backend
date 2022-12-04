from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatListView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('rooms/<int:room_id>', views.ChatRoomView.as_view()),
]
