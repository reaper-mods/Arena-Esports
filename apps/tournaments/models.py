from django.db import models
from django.conf import settings
import uuid

class Game(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='games/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'games'
    
    def __str__(self):
        return self.name

class Tournament(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    TOURNAMENT_TYPES = (
        ('solo', 'Solo'),
        ('duo', 'Duo'),
        ('squad', 'Squad'),
    )
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournaments')
    tournament_type = models.CharField(max_length=20, choices=TOURNAMENT_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='tournaments/')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    max_participants = models.IntegerField()
    prize_pool = models.DecimalField(max_digits=12, decimal_places=2)
    first_prize = models.DecimalField(max_digits=10, decimal_places=2)
    second_prize = models.DecimalField(max_digits=10, decimal_places=2)
    third_prize = models.DecimalField(max_digits=10, decimal_places=2)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    rules = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tournaments'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.game.name}"

class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tournament_registrations')
    team_name = models.CharField(max_length=100, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tournament_registrations'
        unique_together = ('tournament', 'user')
    
    def __str__(self):
        return f"{self.user.full_name} - {self.tournament.name}"

class TournamentResult(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, related_name='result')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tournament_wins')
    runner_up = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tournament_runner_ups')
    second_runner_up = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tournament_third_places', null=True, blank=True)
    announced_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tournament_results'