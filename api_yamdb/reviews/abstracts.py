from django.conf import settings
from django.db import models

class AbstractGenreCategoryModel(models.Model):
    """Абстрактная модель для Genre и Category."""

    name = models.CharField(max_length=settings.MAX_LENGTH_CHARFIELD)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name