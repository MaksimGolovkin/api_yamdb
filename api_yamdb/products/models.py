from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


set_on_delete = 'Удалено'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

<<<<<<< HEAD
    # def __str__(self):
    #     return self.name
=======
    def __str__(self):
        return self.name
>>>>>>> 14bc7076023fd9dbbb0dd71d2bff313029c13e3a


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

<<<<<<< HEAD
    # def __str__(self):
    #     return self.name
=======
    def __str__(self):
        return self.name
>>>>>>> 14bc7076023fd9dbbb0dd71d2bff313029c13e3a


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.IntegerField(default=None, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    genres = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(set_on_delete),
        related_name='titles'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления отзыва', auto_now_add=True, db_index=True)
    score = models.IntegerField(
        'Оценка',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления комментария', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
