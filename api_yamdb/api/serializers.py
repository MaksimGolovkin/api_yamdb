from rest_framework import serializers

from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                "Invalid Username"
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации токена пользователя."""

    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Invalid Username")
        return value
