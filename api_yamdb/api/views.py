from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions,
                            status, viewsets, views, exceptions)
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (AdminPermissions,
                             UserPermissions, UserPermissions)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignupSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from users.models import User
from reviews.models import Category, Genre, Review, Title

NO_PUT_METHODS = ('get', 'post', 'patch', 'delete', 'head', 'options', 'trace')


class CategoryViewSet(CreateModelMixin,
                      ListModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Представление для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        return (AdminPermissions(),)


class GenreViewSet(CreateModelMixin,
                   ListModelMixin,
                   DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Представление для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    search_fields = ('name',)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        return (AdminPermissions(),)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_fields = (
        'category__slug',
        'rating',
        'genre__slug',
        'name',
        'year'
    )

    def get_queryset(self):
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        if genre_slug:
            return Title.objects.filter(genre__slug=genre_slug)
        if category_slug:
            return Title.objects.filter(category__slug=category_slug)
        return super().get_queryset()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        if self.request.method == 'PUT':
            raise MethodNotAllowed('Данный метод запрещен.')

        return (AdminPermissions(),)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        if self.request.method == 'PUT':
            raise MethodNotAllowed('Данный метод запрещен.')

        return (AdminPermissions(),)


@api_view(['POST'])
def signup(request):
    """Функция для регистрации пользователя."""

    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="Код доступа авторизации",
        message=(f"Здравствуйте {user.username},"
                 f"Ваш код доступа: {confirmation_code}"),
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    """Функция для регистрации токена."""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get("username")
    user = get_object_or_404(User, username=username)
    return Response(
        {"Token": str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK
    )


class UsersViewSet(viewsets.ModelViewSet):
    """Представление для модели User."""

    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, AdminPermissions,)

    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PUT')

    def partial_update(self, request, username):
        user = get_object_or_404(User, username=username)
        result = self.get_serializer(user, data=request.data, partial=True)
        result.is_valid(raise_exception=True)
        result.save()
        return Response(result.data)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated, UserPermissions,)
    )
    def get_user_me(self, request):
        user = request.user
        if request.method == 'PATCH':
            result = self.get_serializer(
                user, data=request.data, partial=True)
            result.is_valid(raise_exception=True)
            result.save(role=request.user.role)
            return Response(result.data)
        result = self.get_serializer(request.user)
        return Response(result.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, UserPermissions,)
    http_method_names = NO_PUT_METHODS
    pagination_class = LimitOffsetPagination

    def get_title(self):
        # Отображает объект текущего произведения.
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        # Отображение всех отзывов по произведению.
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        # Создает отзыв для текущего произведения и обновляет рейтинг.
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title
        )
        self.update_title_rating(title)

    def update_title_rating(self, title):
        # Обновляет рейтинг произведения на основе отзывов.
        avg_rating = title.reviews.aggregate(Avg('score'))['score__avg']
        if avg_rating is not None:
            title.rating = round(avg_rating)
        else:
            title.rating = None
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """Предстваление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, UserPermissions,)
    http_method_names = NO_PUT_METHODS
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review,
                                 title=self.kwargs['title_id'],
                                 pk=self.kwargs['review_id'])

    def get_queryset(self):
        # Отображение всех комментариев по отзыву.
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        # Создает комментарий для текузего отзыва.
        serializer.save(author=self.request.user, review=self.get_review())
