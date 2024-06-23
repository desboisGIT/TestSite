from django.core.management.base import BaseCommand
from beats.models import Beats

class Command(BaseCommand):
    help = 'Resets all likes for all beats'

    def handle(self, *args, **kwargs):
        beats = Beats.objects.all()
        for beat in beats:
            beat.likes.clear()
        self.stdout.write(self.style.SUCCESS('Successfully reset likes for all beats'))
        beat = Beats.objects.first()  # Get the first beat instance
        print(beat.view_count)