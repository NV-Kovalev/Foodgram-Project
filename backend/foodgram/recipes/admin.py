from django.contrib import admin

from .models import (
    Tag, Ingredient, IngredientInRecipe,
    Recipe, Favourite, ShoppingCart
)

admin.site.register(IngredientInRecipe)
admin.site.register(Tag)
admin.site.register(Favourite)
admin.site.register(ShoppingCart)


class IngredientInRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInRecipeInLine]
    list_display = ('name', 'author', 'favourites')
    list_filter = ('tags', 'author')
    search_fields = ['name']

    def favourites(self, obj):
        return Favourite.objects.filter(recipe=obj).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ['name']
