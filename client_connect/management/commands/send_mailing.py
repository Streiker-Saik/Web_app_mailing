import smtplib
from typing import Optional

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from client_connect.models import Mailing, Message
from config import settings


class Command(BaseCommand):
    """
    Команда запускает рассылку по первичному ключу, если не указан запускает все
    Методы:
        add_arguments(self, parser):
            Добавляет аргументы команды.
        handle(self, *args, **options) -> None:
            Обрабатывает команду для отправки рассылки
        get_mailing(self, pk: int = None) -> Optional[list]:
            Получает список рассылок. Если указан первичный ключ, возвращает соответствующую рассылку.
        send_mailing(self, mailing: Mailing) -> None:
            Отправляет письма для указанной рассылки.
        send_mail_to_recipient(self, subject: str, body: str, from_email: str, recipient: str) -> None:
            Отправляет письмо указанному получателю.
    """

    help = "Запуск рассылки по первичному ключу, если ключ не указан отправляет все рассылки"

    def add_arguments(self, parser):
        """Добавляет аргументы команды."""
        parser.add_argument("pk", type=int, nargs="?", help="ID рассылки для запуска")

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для отправки рассылки"""

        pk = options.get("pk")
        mailings = self.get_mailing(pk)

        for mailing in mailings:
            self.stdout.write(self.style.SUCCESS(f"Запуск рассылки с ID: {mailing.pk}"))
            self.send_mailing(mailing)

    def get_mailing(self, pk: int = None) -> Optional[list]:
        """Получает список рассылок. Если указан первичный ключ, возвращает соответствующую рассылку."""

        if pk is None:
            mailings = list(Mailing.objects.all())  # получаем все рассылки
            if not mailings:
                self.stdout.write(self.style.ERROR("Нет доступных рассылок для запуска!"))
                return None
            self.stdout.write(self.style.SUCCESS("Запуск всех рассылок..."))
            return mailings
        else:
            try:
                mailing = Mailing.objects.get(pk=pk)  # получаем объект рассылки
                mailings = [mailing]
                self.stdout.write(self.style.SUCCESS(f"Выбрана рассылка с ID: {pk}"))
                return mailings
            except Mailing.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Рассылка с ID: {pk} - не найдена."))
                return None
            except Exception as exc_info:
                self.stdout.write(self.style.ERROR(str(exc_info)))
                return None

    def send_mailing(self, mailing: Mailing) -> None:
        """Отправляет письма для указанной рассылки."""

        message = get_object_or_404(Message, pk=mailing.message.pk)  # Извлекаем сообщение
        subject = message.subject
        body = message.body
        from_email = settings.DEFAULT_FROM_EMAIL
        recipients = mailing.recipients.all()  # Получаем получателей
        recipient_list = [recipient.email for recipient in recipients]
        if not recipient_list:
            self.stdout.write(self.style.WARNING(f"Список получателей для рассылки с ID {mailing.pk} пуст!"))
            return
        for recipient in recipient_list:
            self.send_mail_to_recipient(subject, body, from_email, recipient)

        self.stdout.write(self.style.SUCCESS(f"Рассылка с ID {mailing.pk} выполнена."))

    def send_mail_to_recipient(self, subject: str, body: str, from_email: str, recipient: str) -> None:
        """Отправляет письмо указанному получателю."""
        try:
            send_mail(subject=subject, message=body, from_email=from_email, recipient_list=[recipient])
            self.stdout.write(self.style.SUCCESS(f"Отправлено получателю: {recipient}"))
        except smtplib.SMTPRecipientsRefused as exc_info:
            self.stdout.write(self.style.ERROR(f"Проблема с получателем: {exc_info.recipients}"))
