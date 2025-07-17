from django.db import models

from users.models import CustomUser


class Recipient(models.Model):
    """
    Представление получателя
    Атрибуты:
        email(email): Электронная почта, уникальная
        full_name(str): Ф.И.О., ограничение 150 символами
        comment(str): Комментарий, без ограничений
        owner(ForeignKey): Связь с пользователем, который создал получателя
    """

    email = models.EmailField(unique=True, verbose_name="email")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="owner_recipients", verbose_name="Владелец"
    )

    def __str__(self) -> email:
        """
        Строковое представление получателя
        :return: Электронная почта
        """
        return self.email

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"
        ordering = ["email"]
        permissions = [
            ("can_list_recipients", "Can list recipients"),
        ]


class Message(models.Model):
    """
    Представление сообщения
    Атрибуты:
        subject(str): Тема письма, ограничение 150 символами
        body(str): Тело письма, без ограничений
        owner(ForeignKey): Связь с пользователем, который создал сообщение
    """

    subject: str = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="owner_messages", verbose_name="Владелец"
    )

    def __str__(self) -> str:
        """
        Строковое представление сообщения
        :return: Тема сообщения
        """
        return self.subject

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ["subject"]
        permissions = [
            ("can_list_messages", "Can list messages"),
        ]


class Mailing(models.Model):
    """
    Представление рассылки
    Атрибуты:
        start_time(datetime): Дата и время первой отправки
        end_time(datetime): Дата и время окончания отправки
        status(str): Статус (строка: 'Завершена', 'Создана', 'Запущена'). Возможные значения:
            'done' - рассылка завершена,
            'created' - рассылка создана,
            'launched' - рассылка запущена
        message(ForeignKey): Сообщение (внешний ключ на модель «Сообщение»)
        recipient: Получатели («многие ко многим», связь с моделью «Получатель»)
        owner(ForeignKey): Связь с пользователем, который создал рассылку
    """

    STATUS_CHOICES = [("done", "Завершена"), ("created", "Создана"), ("launched", "Запущена")]
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата первой отправки")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания отправки")
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус", default="created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="mailings", verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, related_name="mailings", verbose_name="Получатели")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="owner_mailings", verbose_name="Владелец"
    )

    def __str__(self) -> str:
        """
        Строковое представление рассылки
        :return: Статус рассылки
        """
        return f"{self.message.subject}: {self.status}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        ordering = ["status"]
        permissions = [
            ("can_list_mailings", "Can list mailings"),
        ]


class SendingAttempt(models.Model):
    """
    Представление попытки рассылки
    Атрибуты:
        created_at(datetime): Дата и время попытки
        status(str): Статус (строка: 'Успешно', 'Не успешно'). Возможные значения:
            'success' - успешно отправлено,
            'fail' - не успешно отправлено,
        answer(str): Ответ почтового сервера (текст)
        mailing(str): Рассылка (внешний ключ на модель «Рассылка»).
    """

    STATUS_CHOICES = [("success", "Успешно"), ("fail", "Не успешно")]
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата попытки отправки")
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    answer = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, related_name="sending_attempts", verbose_name="Рассылка"
    )

    def __str__(self) -> str:
        """
        Строковое представление попытки рассылки
        :return: Статус попытки рассылки
        """
        return self.status

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"
        ordering = ["status"]
        permissions = [("can_list_sending_attempts", "Can_list_sending_attempts")]
