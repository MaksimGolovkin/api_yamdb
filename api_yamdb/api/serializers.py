from rest_framework import serializers
from datetime import date

from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска.')
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        category_data = validated_data.pop('category')

        title = Title.objects.create(category=category_data, **validated_data)

        for genre in genres_data:
            GenreTitle.objects.create(genre=genre, title=title)

        return title

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        ret['category'] = CategorySerializer(instance.category).data
        return ret


class ReviewSerializer(serializers.ModelSerializer):
    """Работа с отзывами."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, value):
        if self.context['request'].method in ['POST']:
            # Проверяем, что произведение существует
            if not Title.objects.filter(id=self.context['view'].kwargs['title_id']).exists():
                raise serializers.ValidationError('Произведение не существует')

            if Review.objects.filter(
                    author=self.context.get('request').user,
                    title=self.context['view'].kwargs['title_id']
            ).exists():
                raise serializers.ValidationError('Not applied many review')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Работа с комментариями."""

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        username = data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                "Invalid Username"
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации токена пользователя."""

    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Invalid Username")
        return value
