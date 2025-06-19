from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("client_connect/", include("client_connect.urls", namespace="client_connect")),
]
