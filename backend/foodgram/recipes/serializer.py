from rest_framework import serializers

from .models import Tags, Ingredients


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        field = ['id', 'name', 'color', 'slug']
        model = Tags


class IngredientsSerizlizer(serializers.ModelSerializer):

    class Meta:
        field = ['id', 'name', 'measurement_unit']
        model = Ingredients
