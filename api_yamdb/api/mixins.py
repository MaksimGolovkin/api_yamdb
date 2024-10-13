from rest_framework import filters, permissions, viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from api.permissions import AdminPermissions

class GenreCategoryMixin(CreateModelMixin,
                   ListModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        return (AdminPermissions(),)