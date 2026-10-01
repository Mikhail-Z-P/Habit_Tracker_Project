from django.core.exceptions import ValidationError
from django.test import TestCase

from habits.models import Habit
from habits.validators import validate_execution_time, validate_periodicity
from users.models import User


class ValidatorTest(TestCase):
    """Тесты standalone-валидаторов."""

    def setUp(self):
        """Создаёт тестового пользователя."""
        self.user = User.objects.create_user(
            username="valuser", email="val@test.com", password="valpass123",
        )

    def test_execution_time_valid(self):
        """Проверка валидного времени выполнения."""
        validate_execution_time(60)

    def test_execution_time_invalid(self):
        """Проверка невалидного времени выполнения."""
        with self.assertRaises(ValidationError):
            validate_execution_time(200)

    def test_periodicity_valid(self):
        """Проверка валидной периодичности."""
        validate_periodicity(3)

    def test_periodicity_invalid(self):
        """Проверка невалидной периодичности."""
        with self.assertRaises(ValidationError):
            validate_periodicity(10)

    def test_habit_with_linked_only(self):
        """Проверка привычки только со связанной привычкой."""
        pleasant = Habit.objects.create(
            user=self.user, place="Дом", time="08:00",
            action="Ванна", is_pleasant=True, execution_time=60,
        )
        habit = Habit(
            user=self.user, place="Дом", time="09:00",
            action="Гулять", linked_habit=pleasant, execution_time=30,
        )
        habit.clean()

    def test_habit_with_reward_only(self):
        """Проверка привычки только с вознаграждением."""
        habit = Habit(
            user=self.user, place="Дом", time="09:00",
            action="Гулять", reward="Сок", execution_time=30,
        )
        habit.clean()
