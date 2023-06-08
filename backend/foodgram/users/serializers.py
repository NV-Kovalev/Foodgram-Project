from rest_framework import serializers
from .models import User, Subscribe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(required=False)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=obj, author=obj).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class SetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class GetTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password', 'email')
