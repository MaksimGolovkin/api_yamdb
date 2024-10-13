from django.db import models

class AbstractGenreCategoryModel(models.Model):
    """Абстрактная модель для Genre и Category."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name