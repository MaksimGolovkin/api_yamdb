from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.models import Category, Genre, Title
from users.admin_mixins import GenreCategoryMixin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'bio',
        'role'
    )
    search_fields = ('username',)
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(GenreCategoryMixin):
    """Админская конфигурация для управления категории."""


@admin.register(Genre)
class GenreAdmin(GenreCategoryMixin):
    """Админская конфигурация для управления жанрами."""


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админская конфигурация для управления произведениями."""

    list_display = ('id', 'name', 'year', 'category', 'description')
    search_fields = ('name', 'year')
    list_filter = ('year', 'category', 'genre')
    empty_value_display = '-пусто-'
    filter_horizontal = ('genre',)
