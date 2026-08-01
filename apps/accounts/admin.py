from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, UserActivity


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'user_type', 'uid', 'is_banned', 'wallet_balance', 'created_at')
    list_filter = ('user_type', 'is_banned', 'is_active', 'created_at')
    search_fields = ('email', 'full_name', 'phone_number', 'uid')
    ordering = ('-created_at',)
    readonly_fields = ('uid', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'is_banned', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Wallet', {'fields': ('wallet_balance',)}),
        ('Identifiers', {'fields': ('uid',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2', 'user_type'),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('uid',)
        return self.readonly_fields


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'user__full_name', 'action')
    readonly_fields = ('user', 'action', 'ip_address', 'timestamp')
    ordering = ('-timestamp',)