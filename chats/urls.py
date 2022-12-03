from django.urls import path
from . import views

urlpatterns = [
    path('/<int:user_id>', views.ChatListView.as_view()),
]
