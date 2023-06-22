from colorfield.fields import ColorField
from django.db import models


class Tags(models.Model):
    """
    Модель тега блюда.
    """
    name = models.CharField(
        'Название тега',
        max_length=96,
        unique=True,
    )
    color = ColorField(
        'Цвет тега в HEX-коде',
        unique=True,
    )
    slug = models.SlugField(
        'Короткое название для использования в URLs',
        max_length=96,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """
    Модель ингредиента.
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=96,
        unique=True
    )
    measurement_unit = models.CharField(
        'Мера измерения ингредиента',
        max_length=16
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
