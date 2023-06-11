from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response

from .models import (
    Ingredient, Tag, Recipe, Favorite, ShoppingCart, RecipeIngredient)
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
                ShoppingCart.objects.create(user=request.user, recipe=queryset)
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
                ShoppingCart, user=request.user, recipe=queryset).delete()
            return Response(
                {'detail': 'Вы успешно убрали рецепт из корзины'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        if not shopping_cart:
            return Response(
                {"detail": "Корзина пуста"},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipes = [item.recipe.id for item in shopping_cart]
        buy_list = RecipeIngredient.objects.filter(
            recipe__in=recipes).values('ingredient').annotate(
            amount=Sum('amount'))
        buy_list_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in buy_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            buy_list_text += (
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )
        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )
        return response
