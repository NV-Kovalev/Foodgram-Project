from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    username = models.CharField(
        'Никнейм пользователя',
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+\Z',
                ('Неправильное значение пользователя '
                 'Это поле может содержать только буквы, '
                 'цифры, а также символы ".@+-"')
            ),
        ],
        error_messages={
            'unique': ('Пользователь с таким никнеймом уже существует'),
        },)
    email = models.EmailField(
        'Электронная почта пользователя',
        unique=True,
        max_length=254,
        error_messages={
            'unique': ('Пользователь с такой электронной почтой '
                       'уже существует'),
        },)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Subscriptions(models.Model):
    """
    Модель Подписок пользователей.
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta():
        unique_together = ('user', 'author',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
