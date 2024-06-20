from django import forms
from .models import Beats

class BeatForm(forms.ModelForm):
    class Meta:
        model = Beats
        fields = ['title', 'genre', 'duration', 'release_date', 'price', 'cover_image', 'audio_file']