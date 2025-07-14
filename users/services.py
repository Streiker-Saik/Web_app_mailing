from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from users.models import CustomUser


class CustomUserService:
    """
    Сервисное класс для работы с пользователями
    Методы:
        activate_by_email(token: str) -> CustomUser:
            Активация пользователя по токену через email.
    """

    @staticmethod
    def activate_by_email(token: str) -> CustomUser:
        """
        Активация пользователя по email
        :param token: Токен активации
        :return: Пользователь с активированный
        """

        user = get_object_or_404(CustomUser, token=token)
        user.is_active = True
        user.save()
        return user

    @staticmethod
    def send_email(subject: str, message: str, user_emails: list) -> None:
        """
        Отправка письма на email
        :param subject: Тема сообщения
        :param message: Текст сообщения
        :param user_emails: Список почты для отправки
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = user_emails
        send_mail(subject, message, from_email, recipient_list)
