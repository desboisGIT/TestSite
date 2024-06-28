# Generated by Django 5.0.6 on 2024-06-23 03:52

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0013_remove_beats_views_beats_likes_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='beats',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='viewed_beats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='beats',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 23, 5, 52, 40, 159661)),
        ),
    ]