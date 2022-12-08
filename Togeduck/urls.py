from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('users.urls')),
    path("workshops/", include('workshops.urls')),
    path("articles/", include('articles.urls')),
    path("chats/", include('chats.urls')),
    # path("accounts/", include('accounts.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)