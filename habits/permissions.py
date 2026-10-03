from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Владелец имеет полный доступ, остальные — только чтение публичных привычек."""

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь владельцем или запрос безопасным."""
        if request.method in SAFE_METHODS and obj.is_public:
            return True
        return obj.user == request.user
