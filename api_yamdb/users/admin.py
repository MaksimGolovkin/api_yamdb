from django.contrib import admin

from users.models import User


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'bio',
        'role'
    )
    search_fields = ('username',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'
