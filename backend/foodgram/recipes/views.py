from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import (
    Tags, Ingredients, Recipe, Favourites, ShoppingCart, IngredientsInRecipe
)
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagsSerializer, IngredientsSerializer,
    CreateRecipeSerializer, RecipeSerializer,
    BasicRecipeSerializer
)
from .pdf_gen import generate_shopping_list_pdf
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
        """
        Функция позволяющая пользователю скачать PDF со списком покупок.
        """

        shopping_list = []
        recipes_id = request.user.shoplist.values_list('recipe', flat=True)

        for recipe_id in recipes_id:
            ingredients = get_object_or_404(
                Recipe, id=recipe_id).ingredients.values()
            for ingredient in ingredients:
                amount = get_object_or_404(
                    IngredientsInRecipe,
                    ingredients_id=ingredient.get('id'),
                    recipe_id=recipe_id).amount
                if not any(item.get('name') == ingredient.get(
                     'name') for item in shopping_list):
                    item = {
                        'name': ingredient.get('name'),
                        'measurement_unit': ingredient.get(
                            'measurement_unit'),
                        'amount': amount
                    }
                    shopping_list.append(item)
                else:
                    for item in shopping_list:
                        if item.get('name') == ingredient.get('name'):
                            item['amount'] += amount

        return generate_shopping_list_pdf(request, shopping_list)
