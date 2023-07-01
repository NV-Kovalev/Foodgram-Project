from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


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


class Recipe(models.Model):
    """
    Модель рецептов, включающая в себя поля связанные many-to-many модели:
    Ingredients и Tags. Модель принимает изображения в Base64 кодировке.
    """
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        verbose_name='Ингредиенты блюда',
        through='IngredientsInRecipe',
        through_fields=('recipe', 'ingredients'),
    )
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги блюда',
    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='recipe',
        null=True,
        default=None
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.IntegerField(
        'Время пригтовления',
        validators=[MinValueValidator(
            1,
            ('Неправильное значение cooking_time '
             'Это поле должно содержать число больше '
             'или равное "1"')
        )]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AbstractRecipeModel(models.Model):
    """
    Абстрактная Модель.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class IngredientsInRecipe(AbstractRecipeModel):
    """
    Модель хранящая ингредиенты и их количество в рецепте.
    """
    ingredients = models.ForeignKey(
        Ingredients,
        verbose_name='Ингредиент в рецепте',
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.FloatField(
        'Количество ингредиента числом',
        validators=[MinValueValidator(
            0,
            ('Неправильное значение amount '
             'Это поле должно содержать число больше "0"')
        )]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredients} в {self.recipe}'


class Favourites(AbstractRecipeModel):
    """
    Модель Избранных рецептов.
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favourites',
    )

    class Meta():
        unique_together = ('user', 'recipe',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(AbstractRecipeModel):
    """
    Модель Корзины Покупок.
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shoplist',
    )

    class Meta():
        unique_together = ('user', 'recipe',)
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'
