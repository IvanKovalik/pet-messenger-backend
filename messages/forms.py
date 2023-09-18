from django import forms

from .models import Message


class NewMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            'text'
        )