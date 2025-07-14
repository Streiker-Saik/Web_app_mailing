from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("client_connect.urls", namespace="client_connect")),
    path("users/", include("users.urls", namespace="users")),
    # path("client_connect/", include("client_connect.urls", namespace="client_connect")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
