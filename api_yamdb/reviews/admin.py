from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Category, Genre, Title

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'bio', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
