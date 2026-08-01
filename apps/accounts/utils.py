import uuid
import hashlib
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import UserActivity


def generate_unique_userid():
    """Generate a unique user ID using UUID4"""
    return uuid.uuid4()


def log_user_activity(user, action, request=None):
    """Log user activities for monitoring"""
    ip_address = None
    if request:
        ip_address = get_client_ip(request)
    
    UserActivity.objects.create(
        user=user,
        action=action,
        ip_address=ip_address
    )


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def send_welcome_email(user):
    """Send welcome email to newly registered user"""
    subject = f'Welcome to {settings.SITE_NAME}!'
    message = f'''
    Hi {user.full_name},
    
    Welcome to ARENA ESPORTS! Your account has been successfully created.
    
    Your Account Details:
    - Email: {user.email}
    - Phone: {user.phone_number}
    
    Start exploring tournaments and join the gaming community!
    
    Best regards,
    ARENA ESPORTS Team
    '''
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
    )


def is_valid_phone_number(phone):
    """Validate phone number format"""
    import re
    pattern = r'^\d{10,15}$'
    return bool(re.match(pattern, phone))


def generate_password_reset_token(user):
    """Generate password reset token"""
    token = hashlib.sha256(
        f"{user.uid}{user.email}{timezone.now()}".encode()
    ).hexdigest()
    return token[:32]


def can_register_for_tournament(user, tournament):
    """Check if user can register for a tournament"""
    from apps.tournaments.models import TournamentRegistration
    
    # Check if user is banned
    if user.is_banned:
        return False, "Your account has been banned."
    
    # Check if already registered
    if TournamentRegistration.objects.filter(tournament=tournament, user=user).exists():
        return False, "You are already registered for this tournament."
    
    # Check registration deadline
    if timezone.now() > tournament.registration_deadline:
        return False, "Registration deadline has passed."
    
    # Check max participants
    current_count = TournamentRegistration.objects.filter(tournament=tournament).count()
    if current_count >= tournament.max_participants:
        return False, "Tournament is full."
    
    # Check wallet balance if entry fee required
    if tournament.entry_fee > 0 and user.wallet_balance < tournament.entry_fee:
        return False, "Insufficient wallet balance."
    
    return True, "Can register"