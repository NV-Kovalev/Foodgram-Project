from rest_framework import serializers

from .models import CustomUser


class CreateUserSeriallizer(serializers.ModelSerializer):

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

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            # 'is_subscribed'
        )
        ordering = ['-pk']
