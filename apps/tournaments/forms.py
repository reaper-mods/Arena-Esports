from django import forms
from .models import Tournament, Game, TournamentRegistration


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name', 'game', 'tournament_type', 'description', 'rules',
            'image', 'start_date', 'end_date', 'registration_deadline',
            'max_participants', 'prize_pool', 'first_prize', 'second_prize',
            'third_prize', 'entry_fee', 'status', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tournament name'
            }),
            'game': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tournament_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tournament description'
            }),
            'rules': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tournament rules'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'registration_deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2
            }),
            'prize_pool': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'first_prize': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'second_prize': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'third_prize': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'entry_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Game name'
            }),
            'icon': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class TournamentRegistrationForm(forms.ModelForm):
    class Meta:
        model = TournamentRegistration
        fields = ['team_name']
        widgets = {
            'team_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Team name (optional)'
            }),
        }