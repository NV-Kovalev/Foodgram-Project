from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import (
    Tags, Ingredients, Recipe, Favourites, ShoppingCart)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagsSerializer, IngredientsSerializer,
    CreateRecipeSerializer, RecipeSerializer,
    BasicRecipeSerializer
)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Обработка list и retrive запросов к Тэгам.
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Обработка list и retrive запросов к Ингредиентам.
    """
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Обработка всех запросов к Рецептам.
    """
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':

            if Favourites.objects.filter(
             user=request.user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже добавлен в избранное"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Favourites.objects.create(user=request.user, recipe=recipe)
            queryset = Recipe.objects.get(id=pk)
            serializer = BasicRecipeSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            if Favourites.objects.filter(
             user=request.user, recipe=recipe).exists():
                Favourites.objects.get(
                    user=request.user, recipe=recipe).delete()
                return Response()
            return Response(
                    {"errors": "Вы не подписаны на этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':

            if ShoppingCart.objects.filter(
             user=request.user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже добавлен в корзину"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            queryset = Recipe.objects.get(id=pk)
            serializer = BasicRecipeSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':

            if ShoppingCart.objects.filter(
             user=request.user, recipe=recipe).exists():
                ShoppingCart.objects.get(
                    user=request.user, recipe=recipe).delete()
                return Response()
            return Response(
                    {"errors": "Вы не добавили этот рецепт в корзину"},
                    status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk):
        ...
