from django.urls import path
from workshops import views


urlpatterns = [ 
    path('', views.WorkshopView.as_view(), name='workshop_view'),
    path('<int:workshop_id>/review/', views.ReviewView.as_view(), name='CommentView'), # 댓글 보기/작성
    path('<int:workshop_id>/review/<int:reviews_id>/', views.ReviewDetailView.as_view(), name='CommentDetailView'), # 댓글 수정/삭제
    path('<int:workshop_id>/', views.WorkshopDetailView.as_view(), name='workshop_detail_view'),
    path('<int:workshop_id>/apply/', views.ApplyView.as_view(), name='apply_view'),
    path('<int:workshop_id>/like/', views.LikeView.as_view(), name='like_view'),
    path('hobby/', views.HobbyView.as_view(), name='hobby_view'),
    path('popular/', views.WorkshopPopularView.as_view(), name='workshop_popular_view'),
    path('location/', views.LocationView.as_view(), name='location_view'),
]

