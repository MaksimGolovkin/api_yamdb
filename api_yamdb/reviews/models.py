from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models

from reviews.abstracts import AbstractGenreCategoryModel
from api.constant import MIN_SCORE, MAX_SCORE
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


class BaseModelReviw(models.Model):
    """Абстрактная модель для добавления текста и даты публикации."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class Review(BaseModelReviw):
    """Класс для работы с отзывами."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Ваша оценка от 1 до 10',
        validators=[MinValueValidator(
                    MIN_SCORE, message=f'Минимальное значение {MIN_SCORE}'),
                    MaxValueValidator(
                    MAX_SCORE, message=f'Максимальное значение {MAX_SCORE}')]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='reviews_unique',
            ),
        )

    def __str__(self):
        return self.text


class Comment(BaseModelReviw):
    """Класс для работы с комметариями."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
