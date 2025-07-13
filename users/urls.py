from django.urls import path
from django.contrib.auth.views import LogoutView

from .apps import UsersConfig
from .views import RegisterView, CustomLoginView, UserActivationView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('email_confirm/<str:token>/', UserActivationView.as_view(), name='email_confirm'),
]
