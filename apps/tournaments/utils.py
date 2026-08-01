from django.utils import timezone
from django.db.models import Count, Q
from .models import Tournament, TournamentRegistration, TournamentResult


def get_active_tournaments():
    """Get currently active tournaments"""
    return Tournament.objects.filter(
        status='ongoing',
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )


def get_upcoming_tournaments():
    """Get upcoming tournaments"""
    return Tournament.objects.filter(
        status='upcoming',
        registration_deadline__gte=timezone.now()
    ).order_by('start_date')


def get_featured_tournaments(limit=5):
    """Get featured tournaments"""
    return Tournament.objects.filter(
        is_featured=True,
        status__in=['upcoming', 'ongoing']
    ).order_by('-start_date')[:limit]


def get_tournament_leaderboard(tournament):
    """Generate leaderboard for a tournament"""
    participants = TournamentRegistration.objects.filter(
        tournament=tournament
    ).select_related('user')
    
    leaderboard = []
    for participant in participants:
        leaderboard.append({
            'user': participant.user,
            'registered_at': participant.registered_at,
            'team_name': participant.team_name,
        })
    
    return sorted(leaderboard, key=lambda x: x['registered_at'])


def check_tournament_capacity(tournament):
    """Check if tournament has available slots"""
    current_count = TournamentRegistration.objects.filter(tournament=tournament).count()
    return current_count < tournament.max_participants


def auto_update_tournament_status():
    """Automatically update tournament statuses based on dates"""
    now = timezone.now()
    
    # Start tournaments
    Tournament.objects.filter(
        status='upcoming',
        start_date__lte=now
    ).update(status='ongoing')
    
    # End tournaments
    Tournament.objects.filter(
        status='ongoing',
        end_date__lte=now
    ).update(status='completed')
    
    # Close registrations
    Tournament.objects.filter(
        registration_deadline__lte=now,
        status__in=['upcoming']
    )


def calculate_prize_distribution(prize_pool, position_count):
    """Calculate prize distribution for positions"""
    if position_count <= 0:
        return []
    
    # Standard distribution: 50%, 30%, 20%
    distribution = []
    if position_count >= 1:
        distribution.append(prize_pool * 0.50)
    if position_count >= 2:
        distribution.append(prize_pool * 0.30)
    if position_count >= 3:
        distribution.append(prize_pool * 0.20)
    if position_count > 3:
        remaining = prize_pool - sum(distribution)
        per_position = remaining / (position_count - 3)
        distribution.extend([per_position] * (position_count - 3))
    
    return distribution


def get_tournament_statistics():
    """Get overall tournament statistics"""
    total_tournaments = Tournament.objects.count()
    active_tournaments = Tournament.objects.filter(status='ongoing').count()
    completed_tournaments = Tournament.objects.filter(status='completed').count()
    total_registrations = TournamentRegistration.objects.count()
    total_prize_pool = Tournament.objects.aggregate(total=models.Sum('prize_pool'))['total'] or 0
    
    return {
        'total_tournaments': total_tournaments,
        'active_tournaments': active_tournaments,
        'completed_tournaments': completed_tournaments,
        'total_registrations': total_registrations,
        'total_prize_pool': total_prize_pool,
    }


def generate_tournament_slug(name):
    """Generate URL-friendly slug from tournament name"""
    import re
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')