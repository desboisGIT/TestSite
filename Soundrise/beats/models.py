from datetime import timezone
from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import *

class Beats(models.Model):
    title = models.CharField(max_length=60)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_beats')  # Add related_name here
    genre = models.CharField(max_length=50)
    duration = models.IntegerField(default=0)
    release_date = models.DateField(default=datetime.now())
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_image = models.ImageField(upload_to='images/beats/')
    audio_file = models.FileField(upload_to='audio/beats/')
    BPM = models.IntegerField(default=0)
    key = models.CharField(default="B♭m", max_length=5)
    description = models.CharField(default="",max_length=500)
    views = models.ManyToManyField(CustomUser, related_name='viewed_beats', blank=True)
    
    def __str__(self):
        return self.title

    def add_view(self, user):
        if user not in self.views.all():
            self.views.add(user)
            return True
        return False

    @property
    def view_count(self):
        return self.views.count()
    