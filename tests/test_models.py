from django.core.exceptions import ValidationError
from django.test import TestCase

from habits.models import Habit
from users.models import User


class HabitModelTest(TestCase):
    """Тесты для модели Habit и её валидаторов."""

    def setUp(self):
        """Создаёт тестового пользователя."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
        )

    def test_create_valid_habit(self):
        """Проверка создания корректной привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Пить воду",
            execution_time=30,
            reward="Съесть конфету",
            periodicity=1,
        )
        self.assertEqual(habit.action, "Пить воду")
        self.assertFalse(habit.is_pleasant)

    def test_create_pleasant_habit(self):
        """Проверка создания приятной привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Принять ванну",
            is_pleasant=True,
            execution_time=60,
        )
        self.assertTrue(habit.is_pleasant)

    def test_validate_reward_and_linked(self):
        """Проверка запрета на связанную привычку и вознаграждение одновременно."""
        pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Принять ванну",
            is_pleasant=True,
            execution_time=60,
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Гулять",
            linked_habit=pleasant,
            reward="Конфета",
            execution_time=30,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_validate_execution_time(self):
        """Проверка ограничения времени выполнения."""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Бегать",
            execution_time=200,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_validate_linked_must_be_pleasant(self):
        """Проверка что связанная привычка должна быть приятной."""
        useful = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Гулять",
            execution_time=30,
            reward="Конфета",
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="09:00",
            action="Читать",
            linked_habit=useful,
            execution_time=30,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_validate_pleasant_no_reward(self):
        """Проверка запрета вознаграждения для приятной привычки."""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Ванна",
            is_pleasant=True,
            reward="Конфета",
            execution_time=30,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_validate_pleasant_no_linked(self):
        """Проверка запрета связанной привычки для приятной."""
        pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Ванна",
            is_pleasant=True,
            execution_time=60,
        )
        habit = Habit(
            user=self.user,
            place="Дом",
            time="09:00",
            action="Чай",
            is_pleasant=True,
            linked_habit=pleasant,
            execution_time=30,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_validate_periodicity(self):
        """Проверка ограничения периодичности."""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Бегать",
            execution_time=30,
            periodicity=10,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_str(self):
        """Проверка строкового представления привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="08:00",
            action="Бегать",
            execution_time=30,
            reward="Сок",
        )
        self.assertIn("Бегать", str(habit))
        self.assertIn("Парк", str(habit))
