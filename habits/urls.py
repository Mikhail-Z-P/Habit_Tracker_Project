from django.urls import path

from habits.views import (
    HabitDetailView,
    HabitListCreateView,
    PublicHabitListView,
)

urlpatterns = [
    path("habits/public/", PublicHabitListView.as_view(), name="habit-public"),
    path("habits/", HabitListCreateView.as_view(), name="habit-list-create"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
]
