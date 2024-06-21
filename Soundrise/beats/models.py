from datetime import timezone
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import *

class Beats(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_beats')  # Add related_name here
    genre = models.CharField(max_length=50)
    duration = models.DurationField()
    release_date = models.DateField(default=datetime.now())
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_image = models.ImageField(upload_to='images/beats/')
    audio_file = models.FileField(upload_to='audio/beats/')