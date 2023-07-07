from rest_framework import serializers

from djoser.serializers import (
    UserSerializer, UserCreateSerializer, SetPasswordSerializer
)
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientInRecipe
)
from users.models import CustomUser


class CreateUserSeriallizer(UserCreateSerializer):
    """
    Сериализатор регистрации пользователя.
    """

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )

    def to_representation(self, instance):
        """Данные которые отправит сервер после запроса"""
        serializer = RepresentationUserSerializer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data


class RepresentationUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор данных о зарегестрировавшемся пользователе.
    """

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name'
        )


class UserSerializer(UserSerializer):
    """
    Сериализатор данных пользователя.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Узнаем подписан ли пользователь на этого автора."""
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(author=obj).exists()


class SetPasswordSerializer(SetPasswordSerializer):
    """
    Сериализатор смены пароля пользователя.
    """
    pass


class BasicRecipeSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор Рецептов для короткого предстваления.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(UserSerializer):
    """
    Cериализатор рецептов и авторов на которых подписан пользователь.
    BasicRecipeSerializer импортирован внутри функции
    для избежания конфликтов импорта.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        """Получаем рецепты автора."""
        queryset = Recipe.objects.filter(author=obj)
        serializer = BasicRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """Считаем рецепты автора."""
        count = Recipe.objects.filter(author=obj.id).count()
        return count

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count',
        )


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор Тэгов.
    """

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор Ингредиентов.
    """

    class Meta:
        model = Ingredient
        fields = ('__all__')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор Ингредиентов в рецепте.
    """
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateIngredientInRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания связи Ингредиентов в рецепте.
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор Рецептов.
    """
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredientinrecipe_set')
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
    ingredients = CreateIngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def validate_ingredients(self, value):
        """Проверяем полученные данные на повторяющиеся элементы."""
        ingredients = []
        for ingredient in value:
            ingredients.append(ingredient.get('id'))
        unique_ingredients = set(ingredients)
        if not len(unique_ingredients) == len(ingredients):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться')
        return value

    def create(self, validated_data):
        """Создаем рецепт и связываем ингредиенты с ним."""
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        data = [
            IngredientInRecipe(
                ingredients=ingredient.get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(data)
        return recipe

    def update(self, instance, validated_data):
        """Изменяем данные о рецепте."""
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            IngredientInRecipe.objects.update_or_create(
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
