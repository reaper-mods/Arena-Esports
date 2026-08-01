from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Tournament, Game, TournamentRegistration
from .forms import TournamentForm

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def tournament_list(request):
    tournaments = Tournament.objects.all().order_by('-start_date')
    featured = Tournament.objects.filter(is_featured=True)[:3]
    
    context = {
        'tournaments': tournaments,
        'featured': featured,
    }
    return render(request, 'tournaments/list.html', context)

def tournament_detail(request, uid):
    tournament = get_object_or_404(Tournament, uid=uid)
    is_registered = False
    
    if request.user.is_authenticated:
        is_registered = TournamentRegistration.objects.filter(
            tournament=tournament, 
            user=request.user
        ).exists()
    
    context = {
        'tournament': tournament,
        'is_registered': is_registered,
    }
    return render(request, 'tournaments/detail.html', context)

@login_required
def tournament_register(request, uid):
    tournament = get_object_or_404(Tournament, uid=uid)
    
    if TournamentRegistration.objects.filter(tournament=tournament, user=request.user).exists():
        messages.warning(request, 'You are already registered for this tournament!')
    else:
        TournamentRegistration.objects.create(
            tournament=tournament,
            user=request.user
        )
        messages.success(request, f'Successfully registered for {tournament.name}!')
    
    return redirect('tournament_detail', uid=uid)

@login_required
@user_passes_test(is_admin)
def admin_tournaments(request):
    tournaments = Tournament.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/tournaments.html', {'tournaments': tournaments})

@login_required
@user_passes_test(is_admin)
def admin_create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.created_by = request.user
            tournament.save()
            messages.success(request, 'Tournament created successfully!')
            return redirect('admin_tournaments')
    else:
        form = TournamentForm()
    
    return render(request, 'admin_panel/tournament_form.html', {'form': form})