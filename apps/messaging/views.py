from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Message
from .forms import MessageForm, BroadcastMessageForm, DirectMessageForm
from .utils import (
    get_user_messages, 
    get_unread_count, 
    send_broadcast_message,
    send_direct_message,
    mark_message_as_read,
    delete_user_messages
)
from apps.accounts.models import User


@login_required
def inbox(request):
    """Display user's inbox"""
    received_messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = get_unread_count(request.user)
    
    context = {
        'messages': received_messages,
        'unread_count': unread_count,
        'page_title': 'Inbox'
    }
    return render(request, 'messaging/inbox.html', context)


@login_required
def sent_messages(request):
    """Display sent messages"""
    sent_msgs = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    context = {
        'messages': sent_msgs,
        'page_title': 'Sent Messages'
    }
    return render(request, 'messaging/sent.html', context)


@login_required
def message_detail(request, message_id):
    """View specific message details"""
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is sender or recipient
    if request.user not in [message.sender, message.recipient]:
        messages.error(request, 'You do not have permission to view this message.')
        return redirect('inbox')
    
    # Mark as read if recipient
    if request.user == message.recipient and not message.is_read:
        mark_message_as_read(message_id, request.user)
    
    context = {
        'message': message,
    }
    return render(request, 'messaging/detail.html', context)


@login_required
def mark_as_read(request, message_id):
    """Mark message as read (AJAX endpoint)"""
    if request.method == 'POST':
        success = mark_message_as_read(message_id, request.user)
        return JsonResponse({'success': success})
    return JsonResponse({'success': False}, status=400)


@login_required
def delete_message(request, message_id):
    """Delete a message"""
    if request.method == 'POST':
        deleted = delete_user_messages(request.user, [message_id])
        if deleted > 0:
            messages.success(request, 'Message deleted successfully.')
        else:
            messages.error(request, 'Message not found.')
    return redirect('inbox')


@login_required
def compose_message(request):
    """Compose and send a new message"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        try:
            recipient = User.objects.get(id=recipient_id)
            send_direct_message(request.user, recipient, subject, content)
            messages.success(request, f'Message sent to {recipient.full_name}!')
            return redirect('sent_messages')
        except User.DoesNotExist:
            messages.error(request, 'Recipient not found.')
    
    users = User.objects.exclude(id=request.user.id)
    context = {
        'users': users,
    }
    return render(request, 'messaging/compose.html', context)


@login_required
def broadcast_message(request):
    """Send broadcast message (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'You do not have permission to broadcast messages.')
        return redirect('inbox')
    
    if request.method == 'POST':
        form = BroadcastMessageForm(request.POST)
        if form.is_valid():
            count = send_broadcast_message(
                request.user,
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                form.cleaned_data['user_type']
            )
            messages.success(request, f'Broadcast sent to {count} users!')
            return redirect('sent_messages')
    else:
        form = BroadcastMessageForm()
    
    context = {
        'form': form,
    }
    return render(request, 'messaging/broadcast.html', context)