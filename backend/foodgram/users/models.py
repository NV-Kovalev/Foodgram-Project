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
                ('Неправильное значение username '
                 'Это поле может содержать только буквы, '
                 'цифры, а также символы ".@+-"')
            ),
        ],
        error_messages={
            'max_length': ('Поле должно быть короче 150 символов'),
        },)
    email = models.EmailField(
        'Электронная почта пользователя',
        unique=True,
        max_length=254,
        error_messages={
            'max_length': ('Поле должно быть короче 150 символов'),
        },)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150,
        error_messages={
            'max_length': ('Поле должно быть короче 150 символов'),
        },)
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150,
        error_messages={
            'max_length': ('Поле должно быть короче 150 символов'),
        },)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

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
