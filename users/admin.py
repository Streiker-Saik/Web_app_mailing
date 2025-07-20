from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с кастомными пользователями
    Атрибуты:
        ordering - сортировка по логику
        list_filter - фильтрация активный пользователь или нет
        exclude - исключит поле пароля
        list_display - выводит на экран: email, логин, имя, фамилия, активный
        search_fields - поиск по: email
    """

    ordering = ("email",)
    list_filter = ("is_active",)
    exclude = ("password",)
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
    )
    search_fields = (
        "email",
    )
