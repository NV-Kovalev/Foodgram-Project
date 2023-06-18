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

    class Meta:
        verbose_name = 'Пользователи'

    def __str__(self):
        return self.email
