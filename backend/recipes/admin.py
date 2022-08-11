from django.contrib import admin

from .models import (Ingredient, IngredientAmount, Recipe,
                     Tag, TagsRecipe
                     )

from .constants import Empty


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagsRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_recipes_favorite')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = Empty
    inlines = [
        TagsInline, IngredientsInline
    ]
    readonly_fields = ['count_recipes_favorite']

    def count_recipes_favorite(self, obj):
        return obj.favorites.count()

    count_recipes_favorite.short_description = 'Популярность'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagsInline
    ]
    list_display = ('name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInline
    ]
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
