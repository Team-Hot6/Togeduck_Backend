from django.urls import path
from articles import views


urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_view'),
    path('recommend/', views.ArticleRecommendView.as_view(), name='article_recommend_view'),
    path('latest/', views.ArticleLatestView.as_view(), name='article_latest_view'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create_view'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name='article_detail_view'),
    path('<int:article_id>/comment/', views.CommentView.as_view(), name='comment_view'),
    path('<int:article_id>/comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment_delete_view'),
]