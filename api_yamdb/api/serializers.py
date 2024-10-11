from datetime import date

from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
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
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ('id', 'name', 'year', 'rating', 'description', 'genres', 'category')
=======
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
>>>>>>> 14bc7076023fd9dbbb0dd71d2bff313029c13e3a
=======
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
>>>>>>> refs/remotes/origin/develop

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска.')
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        category_data = validated_data.pop('category')
        validated_data['category_id'] = category_data.id
        title = Title.objects.create(**validated_data)
        for genre in genres_data:
            pup, status = Genre.objects.get_or_create(id=genre.id, name=genre.name, slug=genre.slug)
            GenreTitle.objects.create(
                genre=pup, title=title
            )
        return title

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['genres'] = GenreSerializer(instance.genres.all(), many=True).data
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



# try:
        #     if 'genres' not in self.initial_data:
        #         title = Title.objects.create(**validated_data)
        #         print(f'1{title}')
        #         return title
        #     genres = validated_data.pop('title')
        #     title = Title.objects.create(**validated_data)
        #     for genre in genres:
        #         current_genre, status = Genre.objects.get_or_create(
        #             **genre
        #         )
        #         GenreTitle.objects.get_or_create(
        #             genre=current_genre, title=title
        #         )
        #     print(f'2{title}')
        #     return title
        # except:
        #     print('Данилу спасибо')