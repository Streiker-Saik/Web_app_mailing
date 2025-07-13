from django.shortcuts import get_object_or_404

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

