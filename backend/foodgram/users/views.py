from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Subscribe
from .serializers import (
    UserSerializer, CreateUserSerializer, SetPasswordSerializer,
    GetTokenSerializer, SubscriptionsSerializer, SubscribeSerializer,
    NewUserResponseSerializer
)


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    ViewSet для перечесления, отображения профилей и регистрации пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create',):
            return CreateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        super(UserViewSet, self).create(request, *args, **kwargs)
        new_user = get_object_or_404(
            User, username=request.data.get('username'))
        serializer = NewUserResponseSerializer(
            new_user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        url_path='me',
        serializer_class=UserSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def user_profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', ],
        detail=False,
        serializer_class=SetPasswordSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        user = get_object_or_404(User, username=request.user)
        if not user.check_password(request.data.get('current_password')):
            return Response(
                {'current_password': 'Неверный пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response(
            {'detail': 'Пароль успешно изменен!'},
            status=status.HTTP_204_NO_CONTENT
            )

    @action(
        methods=['get', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        pagination_class=PageNumberPagination
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionsSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, **kwargs):
        queryset = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                queryset, context={"request": request})
            try:
                Subscribe.objects.create(user=request.user, author=queryset)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception:
                return Response(
                    {'detail': 'Вы уже подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            get_object_or_404(
                Subscribe, user=request.user, author=queryset).delete()
            return Response(
                {'detail': 'Успешная отписка'},
                status=status.HTTP_204_NO_CONTENT
            )


class GetTokenView(viewsets.ModelViewSet):
    """
    ViewSet для получения и удаления токена аунтификации.
    """
    @action(
        methods=['post', ],
        detail=False,
        serializer_class=GetTokenSerializer,
    )
    def login(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        if user.check_password(request.data.get('password')):
            token = RefreshToken.for_user(user)
            return Response(
                {'auth_token': str(token.access_token)},
                status=status.HTTP_201_CREATED)
        return Response(
            data={'detail': 'Неверный логин или пароль.'},
            status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete', ],
        detail=False,
        serializer_class=GetTokenSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def logout(self, request):
        RefreshToken.for_user(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
