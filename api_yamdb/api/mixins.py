from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin,
                                   DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import AdminOrReadOnlyPermissions


class GenreCategoryMixin(CreateModelMixin,
                         ListModelMixin,
                         DestroyModelMixin,
                         viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnlyPermissions,)
    lookup_field = 'slug'
    search_fields = ('name',)
