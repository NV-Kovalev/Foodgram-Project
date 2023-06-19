from rest_framework import serializers

from djoser.serializers import (
    UserSerializer, UserCreateSerializer, SetPasswordSerializer
)

from .models import CustomUser


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
        serializer = RepresentationUserSeriallizer(
            instance, context={'request': self.context.get('request')}
        )
        return serializer.data


class RepresentationUserSeriallizer(serializers.ModelSerializer):
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
    pass


class SubscriptionsSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
            # 'recipes', 'recipes_count',
        )
