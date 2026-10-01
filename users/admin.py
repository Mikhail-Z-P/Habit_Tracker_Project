from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка отображения пользователя в админке."""

    list_display = ("id", "username", "email", "telegram_chat_id")
    search_fields = ("username", "email")
