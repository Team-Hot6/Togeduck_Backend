from django.urls import path
from workshops import views



urlpatterns = [ 
    
    path('', views.WorkshopView.as_view(), name='workshop_view'),
    path('<int:workshop_id>/review/', views.ReviewView.as_view(), name='CommentView'), # 댓글 보기/작성
    path('<int:workshop_id>/review/<int:reviews_id>/', views.ReviewDetailView.as_view(), name='CommentDetailView'), # 댓글 수정/삭제
    
]


