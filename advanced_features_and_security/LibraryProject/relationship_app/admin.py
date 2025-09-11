# relationship_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    list_display = ('email', 'is_staff', 'is_superuser', 'date_of_birth')
    
    # Change the ordering from 'username' to 'email'
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)