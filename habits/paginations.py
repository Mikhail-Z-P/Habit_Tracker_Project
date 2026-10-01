from rest_framework.pagination import LimitOffsetPagination


class HabitPagination(LimitOffsetPagination):
    """Пагинация по схеме limit/offset, 5 привычек на страницу."""

    default_limit = 5
    max_limit = 100
