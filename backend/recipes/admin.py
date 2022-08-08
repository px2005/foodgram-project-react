from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, TagsRecipe)

from .constants import Empty


class IngredientsInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagsRecipe
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = Empty


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = Empty


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
        return obj.favorite_recipes.count()

    count_recipes_favorite.short_description = 'Популярность'

    # list_display = ('id', 'name', 'author', 'amount_favorites',
    #                 'amount_tags', 'amount_ingredients')
    # list_filter = ('author', 'name', 'tags')
    # search_fields = ('name',)
    # empty_value_display = Empty
    #
    # @staticmethod
    # def amount_favorites(obj):
    #     return obj.favorites.count()
    #
    # @staticmethod
    # def amount_tags(obj):
    #     return "\n".join([i[0] for i in obj.tags.values_list('name')])
    #
    # @staticmethod
    # def amount_ingredients(obj):
    #     return "\n".join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = Empty


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = Empty


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = Empty
