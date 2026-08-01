from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content', 'message_type']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message subject'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message here...'
            }),
            'message_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class BroadcastMessageForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Broadcast subject'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Write broadcast message...'
        })
    )
    user_type = forms.ChoiceField(
        choices=[('all', 'All Users'), ('player', 'Players Only'), ('moderator', 'Moderators Only')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class DirectMessageForm(forms.Form):
    recipient = forms.CharField(
        widget=forms.HiddenInput()
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message subject'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Write your message...'
        })
    )