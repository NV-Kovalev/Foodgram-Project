from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import CustomUser, Subscriptions
from .serializers import (
    UserSerializer, CreateUserSeriallizer, SetPasswordSerializer,
    SubscriptionsSerializer
)


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    """
    Класс описывающий: регистрацию пользователя, вывод данных о пользователе,
    смену пароля, возможность подписываться на авторов и вывод списка подписок.
    """
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return UserSerializer
        return CreateUserSeriallizer

    @action(
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def user_profile(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ['post'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = CustomUser.objects.filter(following__user=request.user)
        serializer = SubscriptionsSerializer(
            queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(CustomUser, id=pk)

        if request.method == 'POST':

            if author == request.user:
                return Response(
                    {"errors": "Подписка на себя не доступна"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if Subscriptions.objects.filter(
             user=request.user, author=author).exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Subscriptions.objects.create(user=request.user, author=author)
            queryset = CustomUser.objects.get(username=author.username)
            serializer = SubscriptionsSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            if Subscriptions.objects.filter(
             user=request.user, author=author).exists():
                Subscriptions.objects.get(
                    user=request.user, author=author).delete()
                return Response()
            return Response(
                    {"errors": "Вы уже подписаны на этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST)