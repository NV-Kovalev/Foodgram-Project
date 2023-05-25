from rest_framework.routers import DefaultRouter
from django.urls import path, include


from recipes.views import (
    RecipeViewSet, ShoppingViewSet, DownloadShoppingView, FavoriteViewSet,
    TagViewSet, IngredientViewSet
)
from users.views import UserViewSet, UserRegView, FollowViewSet, GetTokenView


app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register(r'tags', TagViewSet, basename='tags')

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')

router_v1.register(r'recipes', RecipeViewSet, basename='recipes')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    ShoppingViewSet,
    basename='shopping_cart')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite')

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'users/subscriptions', FollowViewSet, basename='subscriptions')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/recipes/download_shopping_cart/',
         DownloadShoppingView.as_view(),
         name='download_shopping_cart'),
    path('v1/auth/signup/', UserRegView.as_view(), name='auth_signup'),
    path('v1/auth/token/', GetTokenView.as_view(), name='token'),
]
