from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким e-mail уже существует.',
            'max_length': 'Адрес должен быть короче 254 символов',
        }
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
            'max_length': 'Никнейм должен быть короче 150 символов',
        }
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        error_messages={
            'max_length': 'Имя должно быть короче 150 символов',
        }
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        error_messages={
            'max_length': 'Фамилия должна быть короче 150 символов',
        }
    )
    password = models.CharField(
        max_length=150,
        error_messages={
            'max_length': 'Пароль должен быть короче 150 символов',
        }
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    def __str__(self):
        return self.username
