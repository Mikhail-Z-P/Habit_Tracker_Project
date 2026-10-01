from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """Модель привычки — полезной или приятной."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
    )
    action = models.CharField(
        max_length=500,
        verbose_name="Действие",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
    )
    execution_time = models.PositiveIntegerField(
        default=60,
        verbose_name="Время на выполнение (секунды)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id"]

    def __str__(self):
        """Возвращает строковое представление привычки."""
        return f"Я буду {self.action} в {self.time} в {self.place}"

    def clean(self):
        """Валидация привычки по бизнес-правилам."""
        errors = {}

        if self.linked_habit and self.reward:
            errors.setdefault("linked_habit", []).append(
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )

        if self.execution_time and self.execution_time > 120:
            errors.setdefault("execution_time", []).append(
                "Время выполнения не должно превышать 120 секунд."
            )

        if self.linked_habit and not self.linked_habit.is_pleasant:
            errors.setdefault("linked_habit", []).append(
                "В связанные привычки можно добавлять только привычки с признаком приятной."
            )

        if self.is_pleasant:
            if self.reward:
                errors.setdefault("reward", []).append(
                    "У приятной привычки не может быть вознаграждения."
                )
            if self.linked_habit:
                errors.setdefault("linked_habit", []).append(
                    "У приятной привычки не может быть связанной привычки."
                )

        if self.periodicity and self.periodicity > 7:
            errors.setdefault("periodicity", []).append(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Сохранение с предварительной валидацией."""
        self.full_clean()
        super().save(*args, **kwargs)
