import django_filters
from rest_framework import filters

from recipes.models import Tag, Recipe


BOOLEAN_CHOICES = (('0', False), ('1', True))


class IngredientCustomSearchFilter(filters.SearchFilter):
    """
    Кастомный фильтр для запросов к ингредиентам.
    """
    search_param = 'name'


class RecipeFilterSet(django_filters.FilterSet):
    """
    Кастомный фильтр для запросов к ингредиентам.
    """
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.TypedChoiceFilter(
        method='get_is_favorited',
        choices=BOOLEAN_CHOICES
    )
    is_in_shopping_cart = django_filters.TypedChoiceFilter(
        method='get_is_in_shopping_cart',
        choices=BOOLEAN_CHOICES
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def get_is_favorited(self, queryset, field_name, value):
        """Фильтруем рецепты по избранным пользователя"""
        return queryset.filter(favourites__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        """Фильтруем рецепты по корзине покупок пользователя"""
        return queryset.filter(shoppingcart__user=self.request.user)
