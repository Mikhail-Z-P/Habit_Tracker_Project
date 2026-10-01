from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Настройка отображения привычек в админке."""

    list_display = (
        "id",
        "user",
        "action",
        "place",
        "time",
        "is_pleasant",
        "is_public",
        "periodicity",
    )
    list_filter = ("is_pleasant", "is_public")
    search_fields = ("action", "place", "user__username")
