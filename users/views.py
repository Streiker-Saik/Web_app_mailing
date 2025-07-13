from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
import secrets

from config import settings
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser
from .services import CustomUserService


class RegisterView(CreateView):
    """
    Кастомное представление регистрации пользователя
    При успешной валидации отправляет письмо пользователю для подтверждения email
    Методы:
        form_valid(self, form: ModelForm) -> HttpResponse:
            Обрабатывает валидную форму и выполняет дополнительное действие
        send_confirmation_email(self, user_email: str, token: str) -> None:
            Отправляет письма с токеном для подтверждения почты
    """

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("client_connect:home")

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """
        Обрабатывает валидную форму и выполняет дополнительное действие
        :param form: Валидная форма содержащая данные пользователя.
        :return: HttpResponse после обработки формы
        """
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        self.send_confirmation_email(user.email, token)
        return super().form_valid(form)

    def send_confirmation_email(self, user_email: str, token: str) -> None:
        """
        Отправляет письма с токеном для подтверждения почты
        :param user_email: Электронная почта пользователя для отправки письма.
        :param token: Электронная почта пользователя для отправки письма.
        """
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}"
        subject = "Подтверждение почты"
        message = f"Для подтверждения почты перейдите по ссылке: {url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class UserActivationView(View):
    """
    Представление активации пользователя
    Методы:
        get(self, request: HttpRequest, token: str) -> HttpResponse:
            Обрабатывает GET запрос для активации пользователя по токену.
        email_verification(self, token: str) -> HttpResponse:
            Активация пользователя по токену.
    """
    def get(self, request: HttpRequest, token: str) -> HttpResponse:
        """
        Обрабатывает GET запрос для активации пользователя по токену.
        :param request: Объект запроса, содержащий информацию о запросе.
        :param token: Токен активации пользователя.
        :return: HttpResponse, содержащий сообщение о статусе активации.
        """
        user = get_object_or_404(CustomUser, token=token)
        if user.is_active:
            return HttpResponse("Пользователь уже активирован", status=200)
        return self.email_verification(token)

    def email_verification(self, token: str) -> HttpResponse:
        """
        Активация пользователя по токену.
        :param token: Токен активации пользователя.
        :return: Перенаправление на страницу входа после успешной активации.
        """
        CustomUserService.activate_by_email(token)
        return redirect(reverse("users:login"))


class CustomLoginView(LoginView):
    """Кастомное представление регистрации пользователя"""

    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("client_connect:home")

