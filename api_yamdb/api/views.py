from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from products.models import Category, Genre, Title, Review, Comment


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_fields = ('category', 'rating', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
   # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Получение всех комментов к отзыву."""
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()
