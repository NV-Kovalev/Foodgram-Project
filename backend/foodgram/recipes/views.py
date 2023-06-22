from rest_framework import viewsets

from .models import Tags, Ingredients
from .serializer import TagsSerializer, IngredientsSerizlizer


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
    serializer_class = IngredientsSerizlizer
