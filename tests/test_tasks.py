from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase

from habits.models import Habit
from habits.services import send_telegram_message
from habits.tasks import send_habit_reminder
from users.models import User


class TelegramServiceTest(TestCase):
    """Тесты сервиса отправки Telegram-сообщений."""

    @patch("habits.services.requests.post")
    def test_send_telegram_success(self, mock_post):
        """Проверка успешной отправки в Telegram."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = send_telegram_message("123456", "Test message")
        self.assertIsNotNone(result)
        mock_post.assert_called_once()

    @patch("habits.services.requests.post")
    def test_send_telegram_failure(self, mock_post):
        """Проверка обработки ошибки отправки."""
        mock_post.side_effect = requests.RequestException("Connection error")
        result = send_telegram_message("123456", "Test message")
        self.assertIsNone(result)


class CeleryTaskTest(TestCase):
    """Тесты Celery-задач."""

    def setUp(self):
        """Создаёт тестового пользователя и привычку."""
        self.user = User.objects.create_user(
            username="taskuser",
            email="task@test.com",
            password="taskpass123",
            telegram_chat_id="123456",
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Парк",
            time="08:00",
            action="Бегать",
            execution_time=30,
            reward="Сок",
        )

    def test_reminder_existing_habit(self):
        """Проверка отправки напоминания для существующей привычки."""
        with patch("habits.tasks.send_telegram_message") as mock_send:
            send_habit_reminder(self.habit.id)
            mock_send.assert_called_once()
            call_args = mock_send.call_args
            self.assertEqual(call_args[0][0], "123456")
            self.assertIn("Бегать", call_args[0][1])

    def test_reminder_nonexistent(self):
        """Проверка для несуществующей привычки."""
        with patch("habits.tasks.send_telegram_message") as mock_send:
            send_habit_reminder(99999)
            mock_send.assert_not_called()

    def test_reminder_no_chat_id(self):
        """Проверка при отсутствии chat_id."""
        self.user.telegram_chat_id = None
        self.user.save()
        with patch("habits.tasks.send_telegram_message") as mock_send:
            send_habit_reminder(self.habit.id)
            mock_send.assert_not_called()
