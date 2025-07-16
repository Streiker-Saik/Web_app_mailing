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
        list_display - выводит на экран: логин, email, имя, фамилия, активный
        search_fields - поиск по: логин, email
    """

    ordering = ("username",)
    list_filter = ("is_active",)
    exclude = ("password",)
    list_display = ("username", "email", "first_name", "last_name", "is_active",)
    search_fields = ("username", "email",)
