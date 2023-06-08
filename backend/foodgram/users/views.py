from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserSerializer, CreateUserSerializer, SetPasswordSerializer,
    GetTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для перечесления, отображения профилей и регистрации пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action in ('create',):
            return CreateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        super(UserViewSet, self).create(request, *args, **kwargs)
        new_user = get_object_or_404(
            User, username=request.data.get('username'))
        custom_response = {
            "email": new_user.email,
            "id": new_user.pk,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
        return Response(custom_response, status=status.HTTP_201_CREATED)

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
        print(request.user.password)
        if user.check_password(request.data.get('current_password')) and (
                request.data.get('new_password') != (
                request.data.get('current_password'))):
            user.set_password(request.data.get('new_password'))
            user.save()


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
        print(request.data.get('password'))
        if user.check_password(request.data.get('password')):
            token = RefreshToken.for_user(user)
            return Response(
                {'auth_token': str(token.access_token)},
                status=status.HTTP_201_CREATED)

    @action(
        methods=['post', ],
        detail=False,
        serializer_class=GetTokenSerializer,
        permission_classes=(IsAuthenticated,)
    )
    def logout(self, request):
        token = RefreshToken.for_user(request.user)
        return Response()
