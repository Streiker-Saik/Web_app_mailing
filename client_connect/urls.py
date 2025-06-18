from django.urls import path
from client_connect.apps import ClientConnectConfig

app_name = ClientConnectConfig.name

urlpatterns = [
    path("_/", _.as_view(), name="_"),
]
