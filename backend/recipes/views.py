from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly
                                        )
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from .filters import RecipeFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoritedSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .download import download_list


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    serializer_class = RecipeSerializer

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve'):
    #         return RecipeListSerializer
    #     return RecipeSerializer

    # @staticmethod
    # def post_method_for_actions(request, pk, serializers):
    #     data = {'user': request.user.id, 'recipe': pk}
    #     serializer = serializers(data=data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # @staticmethod
    # def delete_method_for_actions(request, pk, model):
    #     user = request.user
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     model_obj = get_object_or_404(model, user=user, recipe=recipe)
    #     model_obj.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(detail=True, methods=["POST"],
    #         permission_classes=[IsAuthenticated])
    # def favorite(self, request, pk):
    #     return self.post_method_for_actions(
    #         request=request, pk=pk, serializers=FavoriteSerializer)
    #
    # @favorite.mapping.delete
    # def delete_favorite(self, request, pk):
    #     return self.delete_method_for_actions(
    #         request=request, pk=pk, model=Favorite)
    #
    # @action(detail=True, methods=["POST"],
    #         permission_classes=[IsAuthenticated])
    # def shopping_cart(self, request, pk):
    #     return self.post_method_for_actions(
    #         request=request, pk=pk, serializers=ShoppingCartSerializer)
    #
    # @shopping_cart.mapping.delete
    # def delete_shopping_cart(self, request, pk):
    #     return self.delete_method_for_actions(
    #         request=request, pk=pk, model=ShoppingCart)
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='favorite'
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            favorite_recipe, created = Favorite.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = FavoritedSerializer()
                return Response(
                    serializer.to_representation(instance=favorite_recipe),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            recipe, created = ShoppingCart.objects.get_or_create(
                user=user, recipe=recipe
            )
            if created is True:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже в корзине покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(
                user=user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        try:
            return download_list(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
