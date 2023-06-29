from django.contrib import admin

from .models import (
    Tags, Ingredients, IngredientsInRecipe,
    Recipe, Favourites, ShoppingCart
)

admin.site.register(IngredientsInRecipe)
admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(Favourites)
admin.site.register(ShoppingCart)


class RecipeInIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeInIngredientsInLine, )
