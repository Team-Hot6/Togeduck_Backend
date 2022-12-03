from django.urls import path
from workshops import views


urlpatterns = [
    path('', views.WorkshopView.as_view(), name='workshop_view'),
    path('<int:workshop_id>/', views.WorkshopDetailView.as_view(), name='workshop_detail_view'),
    path('<int:workshop_id>/apply/', views.ApplyView.as_view(), name='apply_view'),
    path('<int:workshop_id>/like/', views.LikeView.as_view(), name='like_view'),
]