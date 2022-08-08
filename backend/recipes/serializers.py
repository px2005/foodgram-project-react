import traceback

from django.db import IntegrityError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient,
                            IngredientAmount, Recipe,
                            ShoppingCart, Tag, TagsRecipe
                            )
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug',)
#
#
# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit',)


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None,
                             use_url=True,)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
                  )

    def get_ingredients(self, obj):
        queryset = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsRecipeSerializer(
        many=True, source='recipe_ingredients'
    )
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(max_value=32767, min_value=1)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_status_func(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        try:
            user = self.context.get('request').user
        except:
            user = self.context.get('user')
        callname_function = format(traceback.extract_stack()[-2][2])
        if callname_function == 'get_is_favorited':
            init_queryset = Favorite.objects.filter(recipe=data.id, user=user)
        elif callname_function == 'get_is_in_shopping_cart':
            init_queryset = ShoppingCart.objects.filter(recipe=data, user=user)
        if init_queryset.exists():
            return True
        return False

    def get_is_favorited(self, data):
        return self.get_status_func(data)

    def get_is_in_shopping_cart(self, data):
        return self.get_status_func(data)

    def create(self, validated_data):
        context = self.context['request']
        ingredients = validated_data.pop('recipe_ingredients')
        try:
            recipe = Recipe.objects.create(
                **validated_data,
                author=self.context.get('request').user
            )
        except IntegrityError as err:
            pass
        tags_set = context.data['tags']
        for tag in tags_set:
            TagsRecipe.objects.create(
                recipe=recipe,
                tag=Tag.objects.get(id=tag)
            )
        ingredients_set = context.data['ingredients']
        for ingredient in ingredients_set:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        context = self.context['request']
        ingredients = validated_data.pop('recipe_ingredients')
        tags_set = context.data['tags']
        recipe = instance
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.tags.set(tags_set)
        IngredientAmount.objects.filter(recipe=instance).delete()
        ingredients_req = context.data['ingredients']
        for ingredient in ingredients_req:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount'],
            )
        return instance

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response

# class RecipeSerializer(serializers.ModelSerializer):
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(), many=True)
#     ingredients = AddIngredientSerializer(many=True)
#     author = CustomUserSerializer(read_only=True)
#     image = Base64ImageField(max_length=None,
#                              use_url=True,)
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'author', 'ingredients', 'tags', 'image',
#             'name', 'text', 'cooking_time'
#         )
#
#     def validate(self, data):
#         ingredients = data['ingredients']
#         ingredients_list = []
#         for ingredient in ingredients:
#             ingredient_id = ingredient['id']
#             if ingredient_id in ingredients_list:
#                 raise serializers.ValidationError({
#                     'ingredients': 'Ингредиенты должны быть уникальными!'
#                 })
#             ingredients_list.append(ingredient_id)
#             amount = ingredient['amount']
#             if int(amount) <= 0:
#                 raise serializers.ValidationError({
#                     'amount': 'Количество ингредиента должно быть больше нуля!'
#                 })
#
#         tags = data.get('tags')
#         if not tags:
#             raise serializers.ValidationError({
#                 'tags': 'Нужно выбрать хотя бы один тэг!'
#             })
#         tags_list = []
#         for tag in tags:
#             if tag in tags_list:
#                 raise serializers.ValidationError({
#                     'tags': 'Тэги должны быть уникальными!'
#                 })
#             tags_list.append(tag)
#
#         cooking_time = data['cooking_time']
#         if int(cooking_time) <= 0:
#             raise serializers.ValidationError({
#                 'cooking_time': 'Время приготовления должно быть больше 0!'
#             })
#         return data
#
#     @staticmethod
#     def create_ingredients(ingredients, recipe):
#         for ingredient in ingredients:
#             IngredientAmount.objects.create(
#                 recipe=recipe, ingredient=ingredient['id'],
#                 amount=ingredient['amount']
#             )
#
#     @staticmethod
#     def create_tags(tags, recipe):
#         for tag in tags:
#             recipe.tags.add(tag)
#
#     def create(self, validated_data):
#         author = self.context.get('request').user
#         tags = validated_data.pop('tags')
#         ingredients = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(author=author, **validated_data)
#         self.create_tags(tags, recipe)
#         self.create_ingredients(ingredients, recipe)
#         return recipe
#
#     def to_representation(self, instance):
#         request = self.context.get('request')
#         context = {'request': request}
#         return RecipeListSerializer(instance, context=context).data
#
#     def update(self, instance, validated_data):
#         instance.tags.clear()
#         IngredientAmount.objects.filter(recipe=instance).delete()
#         self.create_tags(validated_data.pop('tags'), instance)
#         self.create_ingredients(validated_data.pop('ingredients'), instance)
#         return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже есть в избранном!'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
