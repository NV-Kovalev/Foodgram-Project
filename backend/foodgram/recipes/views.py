from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Ingredient, Tag, Recipe, Favorite, ShoppingСart
from api.serializers import (
    IngredientSerializer, TagSerializer, ReadOnlyRecipeSerializer,
    RecipeCreateSerializer, GeneralRecipeSerializer
)

from .permissions import IsAuthorOrReadOnly


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyRecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, **kwargs):
        queryset = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = GeneralRecipeSerializer(
                queryset, context={"request": request})
            try:
                Favorite.objects.create(user=request.user, recipe=queryset)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception:
                return Response(
                    {'detail': 'Вы уже добавили рецепт в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            get_object_or_404(
                Favorite, user=request.user, recipe=queryset).delete()
            return Response(
                {'detail': 'Вы успешно убрали рецепт из избранного'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, **kwargs):
        queryset = get_object_or_404(Recipe, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = GeneralRecipeSerializer(
                queryset, context={"request": request})
            try:
                ShoppingСart.objects.create(user=request.user, recipe=queryset)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception:
                return Response(
                    {'detail': 'Вы уже добавили рецепт в корзину'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            get_object_or_404(
                ShoppingСart, user=request.user, recipe=queryset).delete()
            return Response(
                {'detail': 'Вы успешно убрали рецепт из корзины'},
                status=status.HTTP_204_NO_CONTENT
            )
