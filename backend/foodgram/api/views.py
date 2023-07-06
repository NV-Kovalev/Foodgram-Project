from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from recipes.models import (
    Favourite, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag
)
from users.models import CustomUser, Subscription

from .filters import IngredientCustomSearchFilter, RecipeFilterSet
from .methods import get_post_delete_method
from .pdf_gen import generate_shopping_list_pdf
from .pagination import CustomPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    UserSerializer, CreateUserSeriallizer, SetPasswordSerializer,
    SubscriptionSerializer, TagSerializer, IngredientSerializer,
    CreateRecipeSerializer, RecipeSerializer, BasicRecipeSerializer
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
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от запроса."""
        if self.action in ("retrieve", "list"):
            return UserSerializer
        elif self.action == "set_password":
            return SetPasswordSerializer
        return CreateUserSeriallizer

    @action(
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def user_profile(self, request):
        """Экшн метод для отображения профиля пользователя."""
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        ['post'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        """Экшн метод для изменения пароля пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password'))
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        pagination_class=CustomPaginator
    )
    def subscriptions(self, request):
        """Экшн метод для отображения подписок."""
        queryset = CustomUser.objects.filter(following__user=request.user)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            paginated_queryset, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        """Экшн метод для подписки на других пользователей."""
        return get_post_delete_method(
            self, request, pk, CustomUser, Subscription, UserSerializer
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Обработка list и retrive запросов к Тэгам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Обработка list и retrive запросов к Ингредиентам.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientCustomSearchFilter]
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Обработка запросов к Рецептам.
    """
    queryset = Recipe.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilterSet

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от запроса."""
        if self.action in ("retrieve", "list"):
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        """При создании объекта для поля автора будет использоваться
        текущий пользоваетель."""
        serializer.save(author=self.request.user)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Экшн метод для добавление рецептов в избранное."""
        return get_post_delete_method(
            self, request, pk, Recipe, Favourite, BasicRecipeSerializer)

    @action(
        ['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Экшн метод для добавление рецептов в корзину."""
        return get_post_delete_method(
            self, request, pk, Recipe, ShoppingCart, BasicRecipeSerializer)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Функция позволяющая пользователю скачать PDF со списком покупок."""
        shopping_list = []
        recipes_id = request.user.shoplist.values_list('recipe', flat=True)

        for recipe_id in recipes_id:
            ingredients = get_object_or_404(
                Recipe, id=recipe_id).ingredients.values()
            for ingredient in ingredients:
                amount = get_object_or_404(
                    IngredientInRecipe,
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
