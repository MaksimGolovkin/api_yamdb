from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"

ROLE_CHOICES = (
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
)

user_name_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Username contains invalid characters'
)


class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[user_name_validator]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография', blank=True
    )
    role = models.CharField(
        default=USER,
        verbose_name='Роль',
        max_length=20,
        choices=ROLE_CHOICES
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return f'{self.username}'
