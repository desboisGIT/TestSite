from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=500, default="https://t4.ftcdn.net/jpg/05/17/53/57/360_F_517535712_q7f9QC9X6TQxWi6xYZZbMmw5cnLMr279.jpg")
    profile_free_text = models.CharField(max_length=500, default="Welcome to my profile")
    tel= models.CharField(max_length=20, null=False ,blank=False, default='none')
    mail_pro = models.EmailField(max_length=30,blank=True)


class Beats(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    duration = models.DurationField()
    release_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_image = models.ImageField(upload_to='beats/images/')
    audio_file = models.FileField(upload_to='beats/audio/')

    def __str__(self):
        return self.title