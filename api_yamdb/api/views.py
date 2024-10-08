from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import AdminPermissions, UserPermissions

from users.models import User


from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer
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
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()


class SignupViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get("username")
        email = request.data.get("email")
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
            {"Token": str(AccessToken.for_user(user))}, status=status.HTTP_200_OK
        )


class UsersViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

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
