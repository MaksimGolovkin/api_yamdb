from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constant import MIN_SCORE, MAX_SCORE
from users.models import User

set_on_delete = 'УДАЛЕНО'


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField(
        default=None,
        blank=True,
        null=True,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    description = models.CharField(max_length=256, blank=True, null=True)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(set_on_delete),
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
