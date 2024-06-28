import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=500, default="https://t4.ftcdn.net/jpg/05/17/53/57/360_F_517535712_q7f9QC9X6TQxWi6xYZZbMmw5cnLMr279.jpg")
    profile_free_text = models.CharField(max_length=500, default="Welcome to my profile")
    tel = models.CharField(max_length=20, null=False, blank=False, default='none')
    mail_pro = models.EmailField(max_length=30, blank=True)
    darkTheme = models.BooleanField(default=True)
    rank = models.CharField(default='basic', max_length=30)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    like_number = models.IntegerField(default=0)


    def subscription_count(self):
        return self.followers.count()

    def subscriber_count(self):
        return self.following.count()

    def get_follower_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()

    def is_followed_by_user(self, user):
        return self.followers.filter(id=user.id).exists()

    def liked_beats_count(self):
        return self.liked_beats.count()



