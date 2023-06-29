from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from recipes.views import (
    TagsViewSet, IngredientsViewSet, RecipeViewSet,
)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    r'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    r'tags',
    TagsViewSet,
    basename='tags'
)
router_v1.register(
    r'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
