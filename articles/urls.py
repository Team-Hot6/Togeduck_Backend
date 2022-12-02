from django.urls import path
from articles import views


urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
]