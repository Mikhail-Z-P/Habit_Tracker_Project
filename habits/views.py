from rest_framework import generics

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer, PublicHabitSerializer


class HabitListCreateView(generics.ListCreateAPIView):
    """Список привычек пользователя и создание новых."""

    serializer_class = HabitSerializer

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя."""
        if getattr(self, "swagger_fake_view", False) or self.request.user.is_anonymous:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Сохраняет привычку с текущим пользователем как владельцем."""
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление привычки."""

    serializer_class = HabitSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Возвращает привычки текущего пользователя."""
        if getattr(self, "swagger_fake_view", False) or self.request.user.is_anonymous:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек, только чтение."""

    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        """Возвращает все публичные привычки."""
        return Habit.objects.filter(is_public=True)
