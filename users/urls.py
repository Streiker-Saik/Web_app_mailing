from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path

from .apps import UsersConfig
from .views import CustomLoginView, NewPassword, PasswordRecoveryView, RegisterView, UserActivationView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email_confirm/<str:token>/", UserActivationView.as_view(), name="email_confirm"),
    path("password-reset/", PasswordRecoveryView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path("password-reset/<str:uidb64>/<str:token>/", NewPassword.as_view(), name="password_reset_confirm"),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_complete"
    ),
]
