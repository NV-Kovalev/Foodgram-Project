from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиент."""
    name = models.CharField(
        max_length=96,
        unique=True,
        error_messages={
            'unique': 'Такой ингредиент уже существует.',
            'max_length': 'Поле должно быть короче 96 символов',
        })
    measurement_unit = models.CharField(
        max_length=96,
        error_messages={
            'max_length': 'Поле должно быть короче 96 символов',
        })

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тэг."""
    name = models.CharField(
        max_length=96,
        unique=True,
        error_messages={
            'unique': 'Такое имя уже существует.',
            'max_length': 'Поле должно быть короче 96 символов',
        })
    slug = models.SlugField(
        max_length=96,
        unique=True,
        error_messages={
            'unique': 'Такой слаг уже существует.',
            'max_length': 'Поле должно быть короче 96 символов',
        })
    colour = ColorField(
        'Цвет в HEX',
        format='hex',
        default='#30d5c8',
        unique=True,
        error_messages={
            'unique': 'Такой цвет уже существует.',
            'format': 'Запрос должен быть в HEX-код формате',
        }
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        max_length=200,
        error_messages={
            'max_length': 'Поле должно быть короче 96 символов',
        })
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/image/', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'В {self.recipe} есть {self.ingredient}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]


class Favorite(models.Model):
    "Модель избранных рецептов."
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное'


class ShoppingCart(models.Model):
    "Модель корзины."
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в корзину'
