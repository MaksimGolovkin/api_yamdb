from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from reviews.models import Category, Genre, Title, Review, Comment
from users.admin_mixins import GenreCategoryMixin
from users.models import User


admin.site.empty_value_display = "-пусто-"


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админская конфигурация для управления Пользователями."""

    form = UserChangeForm
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role',)}),
    )
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


@admin.register(Category)
class CategoryAdmin(GenreCategoryMixin):
    """Админская конфигурация для управления категории."""


@admin.register(Genre)
class GenreAdmin(GenreCategoryMixin):
    """Админская конфигурация для управления жанрами."""


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админская конфигурация для управления произведениями."""

    list_display = ('id',
                    'name',
                    'year',
                    'category',
                    'get_genres',
                    'description')
    list_editable = ('category',)
    search_fields = ('name', 'year')
    list_filter = ('year', 'category', 'genre')
    filter_horizontal = ('genre',)

    def get_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all())

    get_genres.short_description = 'Жанры'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админская конфигурация для управления отзывами."""

    list_display = (
        'id',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    search_fields = ('author',)
    list_filter = ('author', 'score', 'pub_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админская конфигурация для управления комментариями."""

    list_display = (
        'id',
        'author',
        'text',
        'pub_date',
        'review'
    )
    search_fields = ('author',)
    list_filter = ('author', 'pub_date')
