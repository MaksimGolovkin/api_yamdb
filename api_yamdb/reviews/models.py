from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.abstracts import AbstractGenreCategoryModel
from users.models import User

SET_ON_DELETE = 'Удалено'


class Category(AbstractGenreCategoryModel):
    """Модель категории."""


class Genre(AbstractGenreCategoryModel):
    """Модель жанра."""


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.DateField(validators=[
        MaxValueValidator(
            date.today().year,
            message='Год не может быть больше текущего'
        )
    ])
    description = models.CharField(max_length=256, blank=True, null=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(SET_ON_DELETE),
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров с произведениями."""

    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='genretitles')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='genretitles')

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
