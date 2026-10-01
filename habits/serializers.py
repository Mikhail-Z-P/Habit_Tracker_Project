from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для CRUD привычек с валидацией через модель."""

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        """Создаёт привычку, привязанную к текущему пользователю."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)

    def validate(self, attrs):
        """Валидирует данные привычки через модельный метод clean."""
        instance = Habit(**attrs)
        instance.clean()
        return attrs


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек, только чтение."""

    class Meta:
        model = Habit
        fields = ("id", "place", "time", "action", "execution_time")
