from django.contrib import admin
from django.utils.html import format_html
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__email', 'recipient__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender', 'recipient', 'message_type', 'subject', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Messages should be created through the app interface