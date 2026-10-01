from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с полем для Telegram chat ID."""

    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Telegram chat ID",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.username
