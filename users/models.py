from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Представление кастомного пользователя, расширяющее AbstractUser.
    Поле авторизации с username изменено на email.
    Так же username обязательное поле при авторизации
    Атрибуты:
        email(str): Уникальный email
        avatar(ImageField): Аватар (изображение)
        phone_number(str): Номер телефона
        country(str): Страна
        token(str): Токен для активации
    """
    username = models.CharField(blank=True, null=True, max_length=150, verbose_name="Логин")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=65, blank=True, null=True, verbose_name="Страна")
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        """
        Строковое представление класса.
        :return: Email
        """
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [
            ("can_list_users", "Can list users"),
            ("can_activate_user", "Can activate user"),
            ("can_deactivate_user", "Can deactivate user"),
        ]
