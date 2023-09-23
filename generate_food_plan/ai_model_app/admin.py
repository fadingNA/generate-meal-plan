from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['id', 'role']
    list_filter = ['role']
    fieldsets = (
        (None, {'fields': ('id', 'password', 'role')}),
        ('Permissions', {'fields': ()}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'password1', 'password2', 'role')}
        ),
    )
    search_fields = ['id']
    ordering = ['id']

