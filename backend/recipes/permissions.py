from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return (request.user.is_superuser
                    or obj.author == request.user)
        return False
