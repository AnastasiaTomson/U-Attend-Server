from rest_framework import serializers
from user.models import User, Student, Teacher, generate_access_token, generate_refresh_token
from django.contrib.auth import authenticate
import secrets


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['login', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    login = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        login = data.get('login', None)
        password = data.get('password', None)
        is_staff = data.get('is_staff', False)

        if login is None:
            raise serializers.ValidationError(
                'Логин не указан'
            )

        if password is None:
            raise serializers.ValidationError(
                'Пароль не указан'
            )

        user = authenticate(username=login, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Неверный логин или пароль'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Пользователь не активен'
            )

        access_token = generate_access_token(user, is_staff)
        refresh_token = generate_refresh_token(user, is_staff)

        return {
            'login': user.login,
            'password': user.password,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
