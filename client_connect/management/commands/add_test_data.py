from django.core.management import call_command
from django.core.management.base import BaseCommand
from client_connect.models import Recipient, Message, Mailing
from users.models import CustomUser


class Command(BaseCommand):
    """Команда для добавления тестовых данных(пользователи, получатели, сообщения, рассылки) из fixture"""

    help = "Add test data(users, recipients, message, mailing) to the database"

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для добавления тестовых данных в базу данных"""
        # Удаляем все существующие
        CustomUser.objects.all().delete()
        Recipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()

        call_command(
            "loaddata",
            (
                "users/fixture/user_fixture.json",
                "client_connect/fixture/recipient_fixture.json",
                "client_connect/fixture/message_fixture.json",
                "client_connect/fixture/mailing_fixture.json",
            ),
        )
        self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры"))
