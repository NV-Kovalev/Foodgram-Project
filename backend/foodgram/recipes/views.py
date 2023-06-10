from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
