from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Класс для работы администратора с кастомными пользователями"""

    exclude = [
        "password",
    ]

