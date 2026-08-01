from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from apps.tournaments.models import Tournament
from apps.messaging.models import Message

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'player'
            user.save()
            
            # Check for admin credentials
            if (user.phone_number == '6666666666' and 
                user.email == 'nikethsureshbabu86@gmail.com'):
                user.user_type = 'admin'
                user.is_staff = True
                user.is_superuser = True
                user.save()
            
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to ARENA ESPORTS!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None and not user.is_banned:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials or account banned.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_tournaments = Tournament.objects.count()
    active_tournaments = Tournament.objects.filter(status='ongoing').count()
    recent_users = User.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_tournaments': total_tournaments,
        'active_tournaments': active_tournaments,
        'recent_users': recent_users,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    query = request.GET.get('q', '')
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'admin_panel/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, uid):
    user = get_object_or_404(User, uid=uid)
    
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.user_type = request.POST.get('user_type')
        user.is_banned = request.POST.get('is_banned') == 'on'
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('admin_users')
    
    return render(request, 'admin_panel/user_edit.html', {'edit_user': user})

@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, uid):
    user = get_object_or_404(User, uid=uid)
    if user.user_type != 'admin':
        user.delete()
        messages.success(request, 'User deleted successfully!')
    else:
        messages.error(request, 'Cannot delete admin users!')
    return redirect('admin_users')

@login_required
@user_passes_test(is_admin)
def admin_ban_user(request, uid):
    user = get_object_or_404(User, uid=uid)
    user.is_banned = not user.is_banned
    user.save()
    status = 'banned' if user.is_banned else 'unbanned'
    messages.success(request, f'User {status} successfully!')
    return redirect('admin_users')

@login_required
@user_passes_test(is_admin)
def admin_send_message(request):
    if request.method == 'POST':
        recipient_uid = request.POST.get('recipient')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        message = Message.objects.create(
            sender=request.user,
            subject=subject,
            content=content,
            message_type='broadcast' if not recipient_uid else 'personal'
        )
        
        if recipient_uid:
            recipient = User.objects.get(uid=recipient_uid)
            message.recipient = recipient
            message.save()
        else:
            # Broadcast to all users
            all_users = User.objects.exclude(uid=request.user.uid)
            for user in all_users:
                Message.objects.create(
                    sender=request.user,
                    recipient=user,
                    subject=subject,
                    content=content,
                    message_type='broadcast'
                )
        
        messages.success(request, 'Message sent successfully!')
        return redirect('admin_messages')
    
    users = User.objects.all()
    return render(request, 'admin_panel/send_message.html', {'users': users})