from django.contrib import admin
from django.utils.html import format_html
from .models import Game, Tournament, TournamentRegistration, TournamentResult


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'game_icon')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    
    def game_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return "No icon"
    game_icon.short_description = 'Icon'


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'tournament_type', 'status', 'prize_pool', 'start_date', 'registrations_count')
    list_filter = ('status', 'tournament_type', 'game', 'is_featured', 'created_at')
    search_fields = ('name', 'game__name')
    ordering = ('-start_date',)
    readonly_fields = ('uid', 'created_at', 'updated_at')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'game', 'tournament_type', 'description', 'rules')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Prizes & Fees', {
            'fields': ('prize_pool', 'first_prize', 'second_prize', 'third_prize', 'entry_fee')
        }),
        ('Settings', {
            'fields': ('max_participants', 'status', 'is_featured', 'image')
        }),
        ('Meta', {
            'fields': ('uid', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def registrations_count(self, obj):
        return obj.registrations.count()
    registrations_count.short_description = 'Registrations'


@admin.register(TournamentRegistration)
class TournamentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'team_name', 'registered_at')
    list_filter = ('registered_at', 'tournament')
    search_fields = ('user__email', 'user__full_name', 'tournament__name')
    ordering = ('-registered_at',)
    readonly_fields = ('registered_at',)


@admin.register(TournamentResult)
class TournamentResultAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'winner', 'runner_up', 'announced_at')
    search_fields = ('tournament__name', 'winner__full_name')
    ordering = ('-announced_at',)
    readonly_fields = ('announced_at',)