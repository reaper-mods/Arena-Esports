from django.db.models import Q
from .models import Message
from apps.accounts.models import User


def get_user_messages(user, message_type=None):
    """Get messages for a specific user"""
    messages = Message.objects.filter(
        Q(recipient=user) | Q(sender=user)
    )
    
    if message_type:
        messages = messages.filter(message_type=message_type)
    
    return messages.order_by('-created_at')


def get_unread_count(user):
    """Get count of unread messages for user"""
    return Message.objects.filter(
        recipient=user,
        is_read=False
    ).count()


def send_broadcast_message(sender, subject, content, user_type='all'):
    """Send broadcast message to users based on type"""
    users = User.objects.all()
    
    if user_type == 'player':
        users = users.filter(user_type='player')
    elif user_type == 'moderator':
        users = users.filter(user_type='moderator')
    
    messages_created = 0
    for user in users:
        if user != sender:
            Message.objects.create(
                sender=sender,
                recipient=user,
                subject=subject,
                content=content,
                message_type='broadcast'
            )
            messages_created += 1
    
    return messages_created


def send_direct_message(sender, recipient, subject, content):
    """Send direct message to specific user"""
    message = Message.objects.create(
        sender=sender,
        recipient=recipient,
        subject=subject,
        content=content,
        message_type='personal'
    )
    return message


def mark_message_as_read(message_id, user):
    """Mark a message as read"""
    try:
        message = Message.objects.get(id=message_id, recipient=user)
        message.is_read = True
        message.save()
        return True
    except Message.DoesNotExist:
        return False


def delete_user_messages(user, message_ids):
    """Delete specified messages for user"""
    deleted_count = Message.objects.filter(
        id__in=message_ids,
        recipient=user
    ).delete()[0]
    return deleted_count


def get_conversation(user1, user2):
    """Get conversation between two users"""
    return Message.objects.filter(
        (Q(sender=user1) & Q(recipient=user2)) |
        (Q(sender=user2) & Q(recipient=user1))
    ).order_by('created_at')