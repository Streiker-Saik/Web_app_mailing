import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.edit import CreateView, FormView

from config import settings
from users.forms import CustomAuthenticationForm, CustomUserCreationForm, NewPasswordForm, PasswordRecoveryForm

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
    success_url = reverse_lazy("users:login")

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


class PasswordRecoveryView(FormView):
    """
    Представление для восстановления пароля по email.
    Методы:
        post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
            Обрабатывает отправку формы с email
        send_password_recovery_email(self, user: CustomUser, token: str) -> None:
            Отправляет электронное письмо для восстановления пароля.
    """

    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_confirm.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:password_reset_done")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обрабатывает отправку формы с email
        :param request: HTTP-запрос
        :param args: дополнительные позиционные аргументы
        :param kwargs: дополнительные именованные аргументы
        :return: HTTP-ответ (редирект или перерисовка формы)
        """

        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            print(email)
            user = CustomUser.objects.get(email=email)
            print(user)
            token = secrets.token_hex(16)
            user.token = token
            user.save()
            self.send_password_recovery_email(user, token)
            return redirect("users:password_reset_done")
        else:
            return render(request, self.template_name, {"form": form})

    def send_password_recovery_email(self, user: CustomUser, token: str) -> None:
        """
        Отправляет электронное письмо для восстановления пароля.
        :param user: Пользователь (экземпляр CustomUser)
        :param token: Токен для сброса пароля
        """

        host = self.request.get_host()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        url = f"http://{host}/users/password-reset/{uidb64}/{token}"
        subject = "Восстановление пароля"
        message = f"Для восстановления пароля перейдите по ссылке: {url}"
        recipient_list = [user.email]
        CustomUserService.send_email(subject, message, recipient_list)


class NewPassword(FormView):
    """
    Представление для сброса пароля пользователя, содержащий uidb64 и токен.
    Методы:
        dispatch(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            Обрабатывает входящие параметры URL и проверяет их валидность.
        get_form_kwargs() -> dict:
            Передает объект пользователя в форму для установки нового пароля.
    """

    template_name = "users/new_password.html"
    form_class = NewPasswordForm
    success_url = reverse_lazy("users:password_complete")

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Обрабатывает входящие параметры URL, декодирует uidb64 в pk пользователя.
        :param request: HTTP-запрос
        :param args: дополнительные позиционные аргументы
        :param kwargs: словарь с параметрами URL ('uidb64', 'token')
        :return: HTTP-ответ (если токен недействителен — сообщение; иначе — продолжение обработки)
        """

        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            self.user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            self.user = None
        if self.user is None or not self.user.token == token:
            return HttpResponse("Пользователя не существует или токен неправильный")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self) -> dict:
        """
        Передает объект пользователя в форму для установки нового пароля.
        :return: Словарь аргументов для формы (включая 'user')
        """

        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs


class CustomLoginView(LoginView):
    """Кастомное представление регистрации пользователя"""

    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("client_connect:home")
