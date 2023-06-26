from django.contrib import admin

from .models import (
    Tags, Ingredients, IngredientsInRecipe,
    Recipe, Favourites, ShoppingCart
)


admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(IngredientsInRecipe)
admin.site.register(Recipe)
admin.site.register(Favourites)
admin.site.register(ShoppingCart)
