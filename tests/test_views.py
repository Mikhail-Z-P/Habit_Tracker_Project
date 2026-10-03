from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habit
from users.models import User


class HabitAPITest(TestCase):
    """Тесты API эндпоинтов привычек."""

    def setUp(self):
        """Создаёт тестовых пользователей и клиент."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="otherpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Проверка создания привычки через API."""
        url = "/api/habits/"
        data = {
            "place": "Парк",
            "time": "08:00",
            "action": "Бегать",
            "execution_time": 30,
            "reward": "Сок",
            "periodicity": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_list_own_habits(self):
        """Проверка что возвращаются только свои привычки."""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Читать",
            execution_time=30,
            reward="Чай",
        )
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="09:00",
            action="Бегать",
            execution_time=30,
            reward="Сок",
        )
        url = "/api/habits/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["action"], "Читать")

    def test_update_own_habit(self):
        """Проверка обновления своей привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Читать",
            execution_time=30,
            reward="Чай",
        )
        url = f"/api/habits/{habit.id}/"
        data = {"place": "Офис"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.place, "Офис")

    def test_delete_own_habit(self):
        """Проверка удаления своей привычки."""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Читать",
            execution_time=30,
            reward="Чай",
        )
        url = f"/api/habits/{habit.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_access_other_user_habit(self):
        """Проверка запрета доступа к чужим привычкам."""
        habit = Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="09:00",
            action="Бегать",
            execution_time=30,
            reward="Сок",
        )
        url = f"/api/habits/{habit.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        """Проверка списка публичных привычек."""
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time="08:00",
            action="Бегать",
            execution_time=30,
            reward="Сок",
            is_public=True,
        )
        Habit.objects.create(
            user=self.other_user,
            place="Дом",
            time="09:00",
            action="Читать",
            execution_time=30,
            reward="Чай",
            is_public=False,
        )
        url = "/api/habits/public/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)

    def test_pagination_structure(self):
        """Проверка структуры пагинации (limit/offset/count/results)."""
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                place=f"Место {i}",
                time="08:00",
                action=f"Действие {i}",
                execution_time=30,
                reward=f"Награда {i}",
            )
        url = "/api/habits/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)


class UserRegistrationTest(TestCase):
    """Тесты эндпоинтов регистрации и авторизации."""

    def setUp(self):
        """Создаёт клиент."""
        self.client = APIClient()

    def test_register_user(self):
        """Проверка регистрации пользователя."""
        url = "/api/register/"
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_password_mismatch(self):
        """Проверка ошибки при несовпадении паролей."""
        url = "/api/register/"
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "password": "strongpass123",
            "password_confirm": "wrongpass",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token(self):
        """Проверка получения JWT-токенов."""
        User.objects.create_user(
            username="logintest",
            email="login@test.com",
            password="loginpass123",
        )
        url = "/api/token/"
        data = {"username": "logintest", "password": "loginpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
