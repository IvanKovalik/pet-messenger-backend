from django import forms

from .models import News


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
            'name',
            'text',
            'image',
            'reading_time'
        )