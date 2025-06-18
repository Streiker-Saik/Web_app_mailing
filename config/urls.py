from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("client_connect/", include("client_connect.urls", namespace="client_connect")),
]
