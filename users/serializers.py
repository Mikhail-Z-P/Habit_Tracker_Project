from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации с подтверждением пароля."""

    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def create(self, validated_data):
        """Создаёт пользователя с хешированным паролем."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        """Проверяет, что пароли совпадают."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных пользователя."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "telegram_chat_id")
