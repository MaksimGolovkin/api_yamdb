from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models

from reviews.abstracts import AbstractGenreCategoryModel
from users.models import User

SET_ON_DELETE = 'Удалено'


class Category(AbstractGenreCategoryModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'

class Genre(AbstractGenreCategoryModel):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=settings.MAX_LENGTH_CHARFIELD)
    year = models.SmallIntegerField(validators=[
        MaxValueValidator(
            date.today().year,
            message='Год не может быть больше текущего'
        )
    ])
    description = models.CharField(
        max_length=settings.MAX_LENGTH_CHARFIELD,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(SET_ON_DELETE)
    )

    class Meta:
        verbose_name = 'Произведение'
        default_related_name = 'titles'
        ordering = ['name', '-year']

    def __str__(self):
        return f'{self.name} {self.description[:20]}'


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров с произведениями."""

    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Промежуточная модель Жанра и Произведения'
        default_related_name = 'genretitles'

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """Класс для работы с отзывами."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1, message='Минимальное значение 1'),
                    MaxValueValidator(10, message='Максимальное значение 10')
                    ]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]


class Comment(models.Model):
    """Класс для работы с комметариями."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
