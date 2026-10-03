import logging

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder(habit_id):
    """Отправляет напоминание о конкретной привычке."""
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        logger.warning("Привычка с id %s не существует", habit_id)
        return

    chat_id = habit.user.telegram_chat_id
    if not chat_id:
        logger.warning("У пользователя %s нет Telegram chat ID", habit.user.username)
        return

    message = f"Напоминаю: я буду {habit.action} " f"в {habit.time} в {habit.place}"
    send_telegram_message(chat_id, message)


@shared_task
def check_and_send_reminders():
    """Проверяет все привычки и отправляет напоминания для тех, чьё время настало."""
    now = timezone.now()
    current_time = now.time()
    current_weekday = now.weekday()

    habits = Habit.objects.filter(is_pleasant=False)

    for habit in habits:
        if habit.periodicity and habit.periodicity > 0:
            if current_weekday % habit.periodicity != 0:
                continue

        if (
            habit.time.hour == current_time.hour
            and habit.time.minute == current_time.minute
        ):
            send_habit_reminder.delay(habit.id)
