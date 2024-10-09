from rest_framework import serializers
from datetime import date

from products.models import Category, Genre, Title, GenreTitle, Review, Comment
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
        fields = ('id', 'name', 'year', 'rating', 'description', 'genres', 'category')

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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title = self.context['view'].get_object()
            author = self.context['request'].user
            if Review.objects.filter(title=title, author=author).count() > 0:
                raise serializers.ValidationError(
                    {'error': 'Нельзя оставить больше 1 отзыва к одному произведению'})
            data['author'] = author
            data['title'] = title

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        review_id = self.context['view'].kwargs.get('review_id')
        if review_id:
            review = get_object_or_404(Review, id=review_id)
            validated_data['review'] = review
        else:
            raise serializers.ValidationError({'review': 'Отзыва нет'})
        return super().create(validated_data)


class SignupSerializer(serializers.ModelSerializer):
    model = User
    fields = ['username', 'email']

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                "Invalid Username"
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(required=True)
    model = User
    fields = ['username', 'confirmation_code']


class UserSerializer(serializers.ModelSerializer):
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