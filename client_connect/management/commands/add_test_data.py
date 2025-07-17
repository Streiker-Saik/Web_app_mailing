from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для добавления тестовых данных(получатели, сообщения, рассылки) из fixture"""

    help = "Add test data(recipients, message, mailing) to the database"

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для добавления продуктов в базу данных"""
        # Удаляем все существующие категории и продукты
        Group.objects.all().delete()

        call_command(
            "loaddata",
            (
                "client_connect/fixture/recipient_fixture.json",
                "client_connect/fixture/message_fixture.json",
                "client_connect/fixture/mailing_fixture.json"
            ),
        )
        self.stdout.write(self.style.SUCCESS("Успешно загружены данные из фикстуры"))
