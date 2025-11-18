from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm

from .models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации пользователя.
    Атрибуты:
        username(str): Логин пользователя, обязательный параметр
        usable_password: Устанавливает параметр для управления паролем
    Методы:
        __init__: Инициализирует поля формы с пользовательскими настройками и атрибутами.
    """

    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs) -> None:
        """Инициализирует поля формы с пользовательскими настройками"""
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Электронная почта"
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )

        self.fields["username"].label = "Логин"
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите уникальный логин"}
        )

        self.fields["password1"].label = "Пароль"
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password1"].help_text = (
            "<ul>"
            "<li>Ваш пароль не может быть слишком похож на другую личную информацию.</li>"
            "<li>Пароль должен содержать не менее 8 символов.</li>"
            "<li>Пароль не может быть слишком распространенным.</li>"
            "<li>Пароль не может состоять только из цифр.</li>"
            "</ul>"
        )

        self.fields["password2"].label = "Подтверждение пароля"
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тот же пароль"})
        self.fields["password2"].help_text = "Введите тот же пароль, что и выше, для проверки."


class UserUpdateForm(forms.ModelForm):
    """
    Форма изменения данных пользователя.
    Методы:
        __init__(self, *args, **kwargs) -> None:
            Инициализирует поля формы с пользовательскими настройками и атрибутами.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "avatar", "phone_number", "country")

    def __init__(self, *args, **kwargs) -> None:
        """Инициализирует поля формы с пользовательскими настройками"""
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Электронная почта"
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите адрес электронной почты"}
        )
        self.fields["username"].label = "Логин"
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите логин"})
        self.fields["first_name"].label = "Имя"
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})
        self.fields["last_name"].label = "Фамилия"
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})

        self.fields["phone_number"].label = "Номер телефона"
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите номер телефона"}
        )
        self.fields["country"].label = "Страна"
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите страну проживания"}
        )


class PasswordRecoveryForm(forms.Form):
    """
    Форма регистрации пользователя.
    Атрибуты:
        email(str): форма email без ограничений
    Методы:
        __init__(self, *args, **kwargs) -> None:
            Инициализирует поля формы с пользовательскими настройками и атрибутами
        clean_email(self) -> str:
            Проверка на существования email.
            :raise ValidationError: Если пользователя не существует в БД
    """

    email = forms.EmailField()

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализирует поля формы с пользовательскими настройками
        :param args: позиционные аргументы
        :param kwargs: именованные аргументы
        """
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Электронная почта"
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите вашу электронную почту"}
        )

    def clean_email(self) -> str:
        """
        Проверка на существования email.
        :return: Email, если существует.
        :raise ValidationError: Если пользователя не существует в БД
        """
        email = self.cleaned_data.get("email")
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Данного пользователя не существует")
        return email


class NewPasswordForm(SetPasswordForm):
    """
    Форма обновления пароля
    Методы:
        __init__(self, *args, **kwargs) -> None:
            Инициализирует поля формы с пользовательскими настройками
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализирует поля формы с пользовательскими настройками
        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)
        self.fields["new_password1"].label = "Пароль"
        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите новый пароль"}
        )
        self.fields["new_password1"].help_text = (
            "<ul>"
            "<li>Ваш пароль не может быть слишком похож на другую личную информацию.</li>"
            "<li>Пароль должен содержать не менее 8 символов.</li>"
            "<li>Пароль не может быть слишком распространенным.</li>"
            "<li>Пароль не может состоять только из цифр.</li>"
            "</ul>"
        )

        self.fields["new_password2"].label = "Подтверждение нового пароля"
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите тот же пароль"}
        )
        self.fields["new_password2"].help_text = "Введите тот же пароль, что и выше, для проверки."


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма авторизации пользователя
    Методы:
        __init__(self, *args, **kwargs) -> None:
            Инициализирует поля формы с пользовательскими настройками и атрибутами
        clean_username(self) -> str:
            Проверка наличие пользователя email
            :raise ValidationError: Если пользователь не зарегистрирован.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Инициализирует поля формы с пользовательскими настройками"""
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите свой email"})
        self.fields["password"].label = "Пароль"
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})

    def clean_username(self) -> str:
        """
        Проверка наличие пользователя email.
        :return: Возвращает email
        :raise ValidationError: Если пользователь не активен.
        """
        email = self.cleaned_data.get("username")
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise forms.ValidationError("Пользователь не активный(возможно вы забыли подтвердить почту)")
            return user.email

        except User.DoesNotExist:
            raise forms.ValidationError("Пользователь с таким email не найден")
