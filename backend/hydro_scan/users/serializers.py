from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    """Сериализатор показа пользователей"""
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователей"""

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'password',
        )
        model = CustomUser
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True}
        }

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def to_representation(self, value):
        return CustomUserSerializer(
            value,
            context=self.context
        ).data


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""
    password = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля для текущего пользователя"""
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)
