from datetime import date


from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from api.constant import WRONGUSERNAME, MAX_LEN_EMAIL, MAX_LEN_USERNAME
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User, user_name_validator


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска.')
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        ret['category'] = CategorySerializer(instance.category).data
        return ret


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, value):
        if self.context['request'].method in ['POST']:
            if Review.objects.filter(
                    author=self.context.get('request').user,
                    title=self.context['view'].kwargs['title_id']
            ).exists():
                raise serializers.ValidationError('Not applied many review')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LEN_USERNAME,
        validators=[user_name_validator]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LEN_EMAIL,
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email):
            return data
        if username == WRONGUSERNAME:
            raise serializers.ValidationError(
                "Invalid Username"
            )
        if User.objects.filter(username=username):
            raise serializers.ValidationError(
                'That username is taken'
            )
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                'That email is taken'
            )
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        user, _ = User.objects.get_or_create(username=username, email=email)
        return user


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации токена пользователя."""

    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('email')
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(
                user, confirmation_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate_username(self, value):
        if value == WRONGUSERNAME:
            raise serializers.ValidationError(
                "Invalid Username")
        return value
