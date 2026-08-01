from django.db import models
from django.conf import settings

class Message(models.Model):
    MESSAGE_TYPES = (
        ('broadcast', 'Broadcast'),
        ('personal', 'Personal'),
    )
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.sender.full_name}"