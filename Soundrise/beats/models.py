from django.db import models
from django.utils import timezone
from django.conf import settings

from accounts.models import CustomUser

class Beats(models.Model):
    title = models.CharField(max_length=60)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded_beats')
    genre = models.CharField(max_length=50)
    duration = models.IntegerField(default=0)
    release_date = models.DateField(default=timezone.now)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_image = models.ImageField(upload_to='images/beats/')
    audio_file = models.FileField(upload_to='audio/beats/')
    BPM = models.IntegerField(default=0)
    key = models.CharField(default="B♭m", max_length=5)
    description = models.CharField(default="", max_length=500)
    views = models.ManyToManyField(CustomUser, related_name='viewed_beats', blank=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_beats', blank=True)
    score = models.FloatField(default=0)
    
    def calculate_score(self):
        # Calculate likes to views ratio
        likes_count = self.likes.count()
        views_count = self.views.count()
        if views_count > 0:
            likes_views_ratio = likes_count / views_count
        else:
            likes_views_ratio = 0

        # Normalize likes to views ratio
        normalized_likes_views_ratio = min(likes_views_ratio, 1.0)  # Cap at 1.0

        # Calculate author's followers compared to site average
        average_followers = self.calculate_average_followers_amount()
        print(average_followers)
        author_followers = self.artist.followers.count()
        if average_followers > 0:
            followers_factor = min(author_followers / average_followers, 2.0)  # Cap at 2 times average
        else:
            followers_factor = 1.0

        # Calculate time decay for views
        days_since_release = (timezone.now().date() - self.release_date).days
        if days_since_release > 0:
            decay_factor = 1 / (1 + days_since_release / 30)  # Adjust 30 for time scale
        else:
            decay_factor = 1.0

        # Combine factors into a final score calculation (adjust weights as needed)
        final_score = (
            normalized_likes_views_ratio * 0.5 +
            followers_factor * 0.3 +
            decay_factor * 0.2
        )

        # Update the score field in the object and save
        self.score = final_score
        self.save()

    @staticmethod
    def calculate_average_followers_amount():
        beatmakers = CustomUser.objects.filter(is_staff=True)  # Assuming all staff users are beat makers
        total_followers = sum(beatmaker.get_follower_count() for beatmaker in beatmakers)
        if beatmakers.exists():
            average_followers_amount = total_followers / len(beatmakers)
        else:
            average_followers_amount = 0
        return average_followers_amount

    def add_like(self, user):
        if user not in self.likes.all():
            self.likes.add(user)
            user.like_number += 1  # Update the user's like number
            user.save()
            self.calculate_score()  # Recalculate score on like addition
            return True
        return False

    def remove_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
            user.like_number -= 1  # Update the user's like number
            user.save()
            self.calculate_score()  # Recalculate score on like removal
            return True
        return False

    def add_view(self, user):
        if user not in self.views.all():
            self.views.add(user)
            self.calculate_score()  # Recalculate score on view addition

    def view_count(self):
        return self.views.count()

    def __str__(self):
        return self.title
    
    
    @property
    def like_count(self):
        return self.likes.count()