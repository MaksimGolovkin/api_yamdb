from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.abstracts import AbstractGenreCategoryModel
from api.constant import MIN_SCORE, MAX_SCORE, MAX_LENGTH_CHARFIELD
from users.models import User

SET_ON_DELETE = 'Удалено'


class Category(AbstractGenreCategoryModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractGenreCategoryModel):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=MAX_LENGTH_CHARFIELD,
                            verbose_name='Название')
    year = models.SmallIntegerField(
        verbose_name='Год',
        validators=[MaxValueValidator(
            date.today().year,
            message='Год не может быть больше текущего'
        )]
    )
    description = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(SET_ON_DELETE),
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ['name', '-year']

    def __str__(self):
        return f'{self.name} {self.description[:20]}'


class GenreTitle(models.Model):
    """Промежуточная модель для связи жанров с произведениями."""

    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Произведение')

    class Meta:
        verbose_name = 'Промежуточная модель Жанра и Произведения'
        default_related_name = 'genretitles'

    def __str__(self):
        return f'{self.genre} {self.title}'


class TextPublicationAuthorModel(models.Model):
    """Абстрактная модель для добавления текста, автора и даты публикации."""

    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.text


class Review(TextPublicationAuthorModel):
    """Класс для работы с отзывами."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text=f'Ваша оценка от {MIN_SCORE} до {MAX_SCORE}',
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
        default_related_name = 'reviews'

class Comment(TextPublicationAuthorModel):
    """Класс для работы с комментариями."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'