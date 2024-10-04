from rest_framework import serializers
from datetime import date

from products.models import Category, Genre, Title, GenreTitle


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
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')

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
