from django import forms
from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    """
    Форма для создания и редактирования получателя.
    Включает все поля
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: email, full_name, comment
    """
    class Meta:
        model = Recipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ф.И.О."})
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Введите комментарий"})



class MessageForm(forms.ModelForm):
    """
    Форма для создания и редактирования сообщений.
    Включает все поля
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: subject, body
    """
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему"})
        self.fields["body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите сообщение"})


class MailingForm(forms.ModelForm):
    """
    Форма для создания и редактирования рассылки.
    Не включает поле status
    Методы __init__(self, *args, **kwargs) -> None:
        Инициализация стилизации форм:
        - стилизация полей: message, recipients
    """

    class Meta:
        model = Mailing
        exclude = ["status"]

    def __init__(self, *args, **kwargs):
        """Инициализация стилизации форм"""
        super().__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-select"})

