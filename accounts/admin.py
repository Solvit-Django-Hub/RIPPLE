from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('RIPPLE Permissions', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('RIPPLE Permissions', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)