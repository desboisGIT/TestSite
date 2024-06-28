# your_app/management/commands/update_beat_scores.py

from django.core.management.base import BaseCommand
from beats.models import Beats 

class Command(BaseCommand):
    help = 'Updates scores for all Beats instances'

    def handle(self, *args, **options):
        beats = Beats.objects.all()
        for beat in beats:
            beat.calculate_score()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated score for Beat: {beat.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully updated scores for all Beats'))
