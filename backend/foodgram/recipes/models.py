from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    """Модель Ингредиент."""
    name = models.CharField(max_length=96, unique=True)
    measurement_unit = models.CharField(max_length=96)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель Тэг."""
    name = models.CharField(max_length=96, unique=True)
    slug = models.SlugField(max_length=96, unique=True)
    colour = ColorField(
        'Цвет в HEX',
        format='hex',
        default='#30d5c8',
        unique=True,
    )

    def __str__(self):
        return self.name
