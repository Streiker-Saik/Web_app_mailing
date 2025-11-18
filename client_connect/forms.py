from django import forms

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя.
    Исключает поле владелец(owner)
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: email, full_name, comment
    """

    class Meta:
        model = Recipient
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ф.И.О."})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})


class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщений.
    Исключает поле владелец(owner)
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: subject, body
    """

    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите сообщение"})


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылки.
    Включает поля: сообщение(message), получатели(recipients)
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: message, recipients
    """

    class Meta:
        model = Mailing
        fields = (
            "message",
            "recipients",
        )

    def __init__(self, *args, **kwargs):
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-select"})
