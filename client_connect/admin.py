from django.contrib import admin

from .models import Mailing, Message, Recipient, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """
    Представление для работы администратора для управления получателями
    Вывод на дисплей: id, email(эл.почта), full_name(ФИО) и comment(комментарий)
    Поиск по email(эл.почта)
    """

    list_display = ("id", "email", "full_name", "comment")
    search_fields = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Представление для работы администратора для управления сообщениями
    Вывод на дисплей: id, subject(заголовок) и body(содержание)
    Поиск по subject(заголовок) и body(содержание)
    """

    list_display = ("id", "subject", "body")
    search_fields = ("subject", "body")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """
    Представление для работы администратора для управления рассылкой
    Вывод на дисплей: id, start_time(дата начала), end_time(дата окончания), status(статус) и message(сообщение)
    Фильтрация по status(статус)
    Сортировка по end_time(дата окончания)
    """

    list_display = ("id", "start_time", "end_time", "status", "message")
    list_filter = ("status",)
    ordering = ("-end_time",)


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    """
    Представление для работы администратора для управления попыткой рассылки
    Вывод на дисплей: id, created_at(дата создания), status(статус), answer(ответ почтового сервера)
    и mailing(рассылка)
    Фильтрация по status(статус)
    Сортировка по created_at(дата и время создания)
    """

    list_display = ("id", "created_at", "status", "answer", "mailing")
    list_filter = ("status",)
    ordering = ("created_at",)
