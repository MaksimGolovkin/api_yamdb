from django.db import models

from api.constant import MAX_LEN_CHARFIELD


class AbstractGenreCategoryModel(models.Model):
    """Абстрактная модель для Genre и Category."""

    name = models.CharField(max_length=MAX_LEN_CHARFIELD,
                            verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name
