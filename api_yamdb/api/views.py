from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import (AdminPermissions,
                             IsAuthorModeratorAdminOrReadOnlyPermission,
                             UserPermissions)
from api.serializers import (CategorySerializer, CommentSerializer, GenreSerializer, 
                             ReviewSerializer, SignupSerializer, TitleSerializer, 
                             TokenSerializer, UserSerializer)
from api.filters import TitleFilter
from api.mixins import GenreCategoryMixin
from reviews.models import Category, Genre, Review, Title
from users.models import User

NO_PUT_METHODS = ('get', 'post', 'patch', 'delete', 'head', 'options', 'trace')


class CategoryViewSet(GenreCategoryMixin):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(GenreCategoryMixin):
    """Представление для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Title.objects.all().annotate(average_rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (AllowAny(),)

        return (AdminPermissions(),)


class SignupViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Представление для регистрации пользователя."""

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        """Проверка на повторный запрос."""
        if User.objects.filter(username=username, email=email):
            user = User.objects.get(username=username, email=email)
        else:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user, user_email = User.objects.get_or_create(
                username=username, email=email
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject="Код доступа авторизации",
            message=(f"Здравствуйте {username},"
                     f"Ваш код доступа: {confirmation_code}"),
            from_email=None,
            recipient_list=[email],
        )
        return Response(request.data, status=status.HTTP_200_OK)


class TokenViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Представление для регистрации токена пользователя."""

    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get("username")
        confirmation_code = request.data.get("confirmation_code")
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"Token": str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )


class UsersViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """Представление для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, AdminPermissions,)

    @action(
        methods=['get', 'patch', 'delete'],
        detail=False,
        url_path=r'(?P<username>[^/.]+)',
        permission_classes=(IsAuthenticated, AdminPermissions,)
    )
    def get_user_username(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            result = self.get_serializer(user, data=request.data, partial=True)
            result.is_valid(raise_exception=True)
            result.save()
            return Response(result.data)
        if request.method == 'DELETE':
            user.delete()
            message = 'Пользователь удален'
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        result = self.get_serializer(user)
        return Response(result.data)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path=r'me',
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
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)
    http_method_names = NO_PUT_METHODS
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Отображает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Отображение всех отзывов по произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает отзыв для текущего произведения и обновляет рейтинг."""
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title
        )
        self.update_title_rating(title)

    # def update_title_rating(self, title):
    #     """Обновляет рейтинг произведения на основе отзывов."""
    #     avg_rating = title.reviews.aggregate(Avg('score'))['score__avg']
    #     if avg_rating is not None:
    #         title.rating = round(avg_rating)
    #     else:
    #         title.rating = None
    #     title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """Предстваление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)
    http_method_names = NO_PUT_METHODS
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review,
                                 title=self.kwargs['title_id'],
                                 pk=self.kwargs['review_id'])

    def get_queryset(self):
        """Отображение всех комментариев по отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текузего отзыва."""
        serializer.save(author=self.request.user, review=self.get_review())
