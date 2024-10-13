from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from users.models import User


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
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
    empty_value_display = '-пусто-'
