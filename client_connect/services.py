import smtplib
from typing import Optional, Callable

from django.core.mail import send_mail
from django.db.models import Model
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from client_connect.models import Mailing, Message, SendingAttempt
from config import settings
from config.settings import CACHE_ENABLED
from users.models import CustomUser


class DecoratorsService:
    """
    Сервисный класс для работы с декораторами
    Методы:
        get_cache_decorator(cached_enable: bool = CACHE_ENABLED, minutes: int = 15) -> Callable:
            Возвращает декоратор для кеширования.
    """

    @staticmethod
    def get_cache_decorator(cached_enable: bool = CACHE_ENABLED, minutes: int = 5) -> Callable:
        """
        Возвращает декоратор для кеширования.
        :param cached_enable: Включение кеширования(по умолчанию config.settings.CACHE_ENABLED).
        :param minutes: Минуты, сколько храниться кеш(по умолчанию 5 минут).
        :return: Декоратор для кеширования.
        """
        if cached_enable:
            cache_decorator = method_decorator(cache_page(60 * minutes), name="dispatch")
        else:
            cache_decorator = lambda view: view
        return cache_decorator


class AccessControlService:
    """
    Сервисный класс для работы с правами доступа
    Методы:
        can_access_object(user: CustomUser, obj: Model, permission_name: str = None) -> bool:
            Проверяет, имеет ли пользователь право выполнить действие над объектом. Создатель имеет право.
        authorize_access(user: CustomUser, obj: Model, permission_name: str = None) -> Optional[HttpResponseForbidden]:
            Проверяет право доступа пользователя к выполнению действия над объектом.
        can_create_object(user: CustomUser, permission_name: str = None) -> bool:
            Проверка на право доступа к созданию объекта
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
        if owner is None and not user.groups.exists():
            return True
        if owner == user:
            return True
        if permission_name:
            return user.has_perm(permission_name)
        return False

    @staticmethod
    def authorize_access(user: CustomUser, obj: Model, permission_name: str = None) -> Optional[HttpResponseForbidden]:
        """
        Проверяет право доступа пользователя к выполнению действия над объектом.
        :param user: Пользователь, который пытается выполнить действие.
        :param obj: Объект, который нужно проверить
        :param permission_name: Название разрешения
        :return: HttpResponseForbidden, если доступ запрещен.
        """

        if not AccessControlService.can_access_object(user, obj, permission_name):
            return HttpResponseForbidden("У вас нет прав на выполнение этого действия")
        return None

    @staticmethod
    def can_create_object(user: CustomUser, permission_name: str = None) -> bool:
        """
        Проверка на право доступа к созданию объекта
        :param user: Пользователь, который пытается выполнить действие.
        :param permission_name: Название разрешения
        :return: True, если пользователь не состоит в группе и имеет разрешение, иначе False
        """

        if user.groups.exists():
            return user.has_perm(permission_name)
        else:
            return True


class MailingService:
    """
    Сервисный класс для работы с рассылкой
    Методы:
        update_status(mailing: Mailing, status: str = "created") -> None:
            Обновляет статус рассылки и фиксирует временные метки.
        send_messages(recipients: list, message: Message, mailing: Mailing) -> None:
            Отправляет сообщения получателям и фиксирует результаты.
    """

    @staticmethod
    def update_status(mailing: Mailing, status: str = "created") -> None:
        """
        Обновляет статус рассылки и фиксирует временные метки.
        :param mailing: Модель рассылки.
        :param status: Статус рассылки(по умолчанию created - создана)
        """
        if status == "launched":
            mailing.start_time = timezone.now()
        elif status == "done":
            mailing.end_time = timezone.now()
        mailing.status = status
        mailing.save()

    @staticmethod
    def send_messages(recipients: list, message: Message, mailing: Mailing) -> None:
        """
        Отправляет сообщения получателям и фиксирует результаты.
        С проверкой статуса, если отключена, то останавливает цикл.
        :param recipients: Список получателей.
        :param message: Модель сообщения.
        :param mailing: Модель рассылки.
        """
        subject = message.subject
        message = message.body
        for recipient in recipients:
            try:
                from_email = settings.DEFAULT_FROM_EMAIL
                if mailing.status == "disable":
                    break
                send_mail(subject, message, from_email, [recipient])
            except smtplib.SMTPException as exc_info:
                SendingAttempt.objects.create(status="fail", answer=str(exc_info), mailing=mailing)
            else:
                SendingAttempt.objects.create(status="success", answer="Сообщение успешно отправлено", mailing=mailing)
