from rest_framework import viewsets, mixins

from .models import CustomUser
from .serializers import (
    UserSerializer, CreateUserSeriallizer
)


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.ReadOnlyModelViewSet
):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return UserSerializer
        return CreateUserSeriallizer

    """
    def create(self, request):
        serializer = CreateUserSeriallizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RepresentationUserSeriallizer(
            data=request.data, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    """
