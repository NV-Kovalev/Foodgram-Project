from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=96,
        verbose_name='Название ингредиента'
    )
    unit = models.CharField(
        related_name='ingredient_unit',
        verbose_name='Единица измерения'
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipe_author'
    )
