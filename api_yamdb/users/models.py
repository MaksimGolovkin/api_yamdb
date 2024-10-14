from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from api.constant import (
    USER, ADMIN, MODERATOR, REGEXUSERNAME, WRONGUSERNAME,
    MAX_LEN_USERNAME, MAX_LEN_EMAIL
)


ROLE_CHOICES = (
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
)

# Проверка на корректность ввода.
user_name_validator = RegexValidator(
    regex=REGEXUSERNAME,
    message='Username contains invalid characters'
)


class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=MAX_LEN_USERNAME,
        unique=True,
        validators=[user_name_validator]
    )
    email = models.EmailField(
        max_length=MAX_LEN_EMAIL,
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография', blank=True
    )
    role = models.CharField(
        default=USER,
        verbose_name='Роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("role",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username=WRONGUSERNAME),
                name='username_not_me'
            )
        ]

    def __str__(self):
        return f'{self.username}'
