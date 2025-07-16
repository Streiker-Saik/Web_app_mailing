from typing import Optional

from django.db.models import Model
from django.http import HttpResponseForbidden

from users.models import CustomUser


class AccessControlService:
    """
    Сервисный класс для работы с правами доступа
    Методы:
        can_access_object(user: CustomUser, obj: Model, permission_name: str = None) -> bool:
            Проверяет, имеет ли пользователь право выполнить действие над объектом. Создатель имеет право.
        authorize_access(user: CustomUser, obj: Model, permission_name: str = None) -> Optional[HttpResponseForbidden]:
            Проверяет право доступа пользователя к выполнению действия над объектом.
    """

    @staticmethod
    def can_access_object(user: CustomUser, obj: Model, permission_name: str = None) -> bool:
        """
        Проверяет, имеет ли пользователь право выполнить действие над объектом.
        Создатель имеет право.
        :param user: Пользователь, который пытается выполнить действие.
        :param obj: Объект, который нужно проверить на право редактирования.
        :param permission_name: Название разрешения
        :return: True, если пользователь имеет право, иначе False
        """

        # Получаем владельца объекта
        owner = getattr(obj, "owner", None)
        if owner == user:
            return True
        if permission_name:
            return user.has_perm(permission_name)
        return False

    @staticmethod
    def authorize_access(user: CustomUser, obj: Model, permission_name: str = None) -> Optional[HttpResponseForbidden]:
        """
        Проверяет право доступа пользователя к выполнению действия над объектом.
        :param user:
        :param obj: Объект, который нужно проверить
        :param permission_name: Название разрешения
        :return: HttpResponseForbidden, если доступ запрещен.
        """

        if not AccessControlService.can_access_object(user, obj, permission_name):
            return HttpResponseForbidden("У вас нет прав на выполнение этого действия")
        return None
