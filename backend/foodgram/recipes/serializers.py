from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from .models import (
    Tags, Ingredients, Recipe, IngredientsInRecipe)
from users.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    """
    Сериализатор Тэгов.
    """

    class Meta:
        model = Tags
        fields = ('__all__')


class IngredientsSerializer(serializers.ModelSerializer):
    """
    Сериализатор Ингредиентов.
    """

    class Meta:
        model = Ingredients
        fields = ('__all__')


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор Ингредиентов в рецепте.
    """
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateIngredientsInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания связи Ингредиентов в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all())

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор Рецептов.
    """
    tags = TagsSerializer(many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Узнаем добавлен ли рецепт в избранное."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favourites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Узнаем добавлен ли рецепт в корзину."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shoplist.filter(recipe=obj).exists()

    def get_ingredients(self, obj):
        """Получаем ингредиенты в рецепте и их количество."""
        queryset = IngredientsInRecipe.objects.filter(recipe=obj)
        serializer = IngredientsInRecipeSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )


class CreateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания Рецептов.
    """
    ingredients = CreateIngredientsInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        """Создаем рецепт и связываем ингредиенты с ним."""
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        for ingredient in ingredients:
            IngredientsInRecipe.objects.create(
                ingredients=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        """Изменяем данные о рецепте."""
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            IngredientsInRecipe.objects.update_or_create(
                ingredients=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=instance
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Данные которые отправит сервер после запроса"""
        serializer = RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data


class BasicRecipeSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор Рецептов для короткого предстваления.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
