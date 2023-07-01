from django.contrib import admin

from .models import (
    Tags, Ingredients, IngredientsInRecipe,
    Recipe, Favourites, ShoppingCart
)

admin.site.register(IngredientsInRecipe)
admin.site.register(Tags)
admin.site.register(Favourites)
admin.site.register(ShoppingCart)


class RecipeInIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeInIngredientsInLine, )
    list_display = ('name', 'author', 'favourites')
    list_filter = ('tags', 'author')
    search_fields = ['name']

    def favourites(self, obj):
        result = Favourites.objects.filter(recipe=obj).count()
        return result


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ['name']
