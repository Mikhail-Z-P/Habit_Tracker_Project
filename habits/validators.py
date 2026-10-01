from django.core.exceptions import ValidationError


def validate_execution_time(value):
    """Проверяет, что время выполнения не превышает 120 секунд."""
    if value > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_periodicity(value):
    """Проверяет, что периодичность не превышает 7 дней."""
    if value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
