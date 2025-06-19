from django.db import models


class Recipient(models.Model):
    """
    Представление получателя
    Атрибуты:
        email(email): Электронная почта, уникальная
        full_name(str): Ф.И.О., ограничение 150 символами
        comment(str): Комментарий, без ограничений
    """

    email = models.EmailField(unique=True, verbose_name="email")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий")

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


class Message(models.Model):
    """
    Представление сообщения
    Атрибуты:
        subject(str): Тема письма, ограничение 150 символами
        body(str): Тело письма, без ограничений
    """

    subject: str = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

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


class Mailing(models.Model):
    """
    Представление рассылки
    Атрибуты:
        created_at(datetime): Дата и время первой отправки
        update_at(datetime): Дата и время окончания отправки
        status(str): Статус (строка: 'Завершена', 'Создана', 'Запущена'). Возможные значения:
            'done' - рассылка завершена,
            'created' - рассылка создана,
            'launched' - рассылка запущена
        message(fk): Сообщение (внешний ключ на модель «Сообщение»)
        recipient: Получатели («многие ко многим», связь с моделью «Получатель»).
    """

    STATUS_CHOICES = [("done", "Завершена"), ("created", "Создана"), ("launched", "Запущена")]
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первой отправки")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата окончания отправки")
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="mailings", verbose_name="Сообщение")
    recipient = models.ManyToManyField(Recipient, related_name="mailings", verbose_name="Получатель")

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


class SendingAttempt(models.Model):
    """
    Представление попытки рассылки
    Атрибуты:
        created_at(datetime): Дата и время попытки
        status(str): Статус (строка: 'Успешно', 'Не успешно'). Возможные значения:
            'suc' - успешно отправлено,
            'fail' - не успешно отправлено,
        answer(str): Ответ почтового сервера (текст)
        mailing(str): Рассылка (внешний ключ на модель «Рассылка»).
    """

    STATUS_CHOICES = [("suc", "Успешно"), ("fail", "Не успешно")]
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
