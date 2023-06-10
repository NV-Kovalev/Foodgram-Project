from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    """Кастомная user модель."""
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
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
            'max_length': 'Никнейм должен быть короче 150 символов',
        }
    )
    first_name = models.CharField(
        max_length=150,
        error_messages={
            'max_length': 'Имя должно быть короче 150 символов',
        }
    )
    last_name = models.CharField(
        max_length=150,
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
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки на авторов."""
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')
        ]

    def __str__(self):
        return f'{self.user} подписка на {self.author}'
