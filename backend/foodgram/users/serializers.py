from rest_framework import serializers

from djoser.serializers import (
    UserSerializer, UserCreateSerializer, SetPasswordSerializer
)

from .models import CustomUser
from recipes.models import Recipe


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
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(author=obj).exists()


class SetPasswordSerializer(SetPasswordSerializer):
    """
    Сериализатор смены пароля пользователя.
    """
    pass


class SubscriptionsSerializer(UserSerializer):
    """
    Cериализатор рецептов и авторов на которых подписан пользователь.
    BasicRecipeSerializer импортирован внутри функции
    для избежания конфликтов импорта.
    """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        from recipes.serializers import BasicRecipeSerializer
        queryset = Recipe.objects.filter(author=obj)
        serializer = BasicRecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        count = Recipe.objects.filter(author=obj.id).count()
        return count

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count',
        )
