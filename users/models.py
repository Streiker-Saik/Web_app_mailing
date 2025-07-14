from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Представление кастомного пользователя, расширяющее AbstractUser.
    Email обязательное поле при авторизации
    Атрибуты:
        email(str): Уникальный email
        token(str): Токен для активации
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        """
        Строковое представление класса.
        :return: Логин(email)
        """
        return f"{self.username}({self.email})"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
