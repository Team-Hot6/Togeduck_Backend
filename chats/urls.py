from django.urls import path
from . import views

urlpatterns = [
    path('', views.LobbyView.as_view()),
]
