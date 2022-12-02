from django.urls import path
from workshops import views



urlpatterns = [ 
    

    path('<int:workshop_id>/comment/', views.ReviewView.as_view(), name='CommentView'), # 댓글 보기/작성
    path('<int:workshop_id>/comment/<int:reviews_id>/', views.ReviewDetailView.as_view(), name='CommentDetailView'), # 댓글 수정/삭제
    
]
