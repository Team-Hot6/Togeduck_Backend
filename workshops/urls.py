from django.urls import path
from workshops import views


urlpatterns = [
    path('', views.WorkshopView.as_view(), name='workshop_view'),
]