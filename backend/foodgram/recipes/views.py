from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import (
    Tags, Ingredients, Recipe, Favourites, ShoppingCart)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagsSerializer, IngredientsSerializer,
    CreateRecipeSerializer, RecipeSerializer,
    BasicRecipeSerializer
)
from users.custom_methods import get_post_delete_method


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
        return get_post_delete_method(
            self, request, pk, recipe, Favourites, BasicRecipeSerializer)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return get_post_delete_method(
            self, request, pk, recipe, ShoppingCart, BasicRecipeSerializer)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ...
