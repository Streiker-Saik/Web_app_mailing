from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Представление кастомного пользователя, расширяющее AbstractUser.
    Email обязательное поле при авторизации
    Атрибуты:
        email(str): Уникальный email
        avatar(ImageField): Аватар (изображение)
        phone_number(str): Номер телефона
        country(str): Страна
        token(str): Токен для активации
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=65, blank=True, null=True, verbose_name="Страна")
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
        permissions = [
            ("can_list_users", "Can list users"),
            ("can_activate_user", "Can activate user"),
            ("can_deactivate_user", "Can deactivate user"),
        ]
