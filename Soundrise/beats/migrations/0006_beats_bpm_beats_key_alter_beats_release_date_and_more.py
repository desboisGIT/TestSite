# Generated by Django 5.0.6 on 2024-06-22 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0005_alter_beats_duration_alter_beats_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='beats',
            name='BPM',
            field=models.IntegerField(default=0, max_length=3),
        ),
        migrations.AddField(
            model_name='beats',
            name='key',
            field=models.CharField(default='B♭m', max_length=5),
        ),
        migrations.AlterField(
            model_name='beats',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 22, 19, 24, 8, 303995)),
        ),
        migrations.AlterField(
            model_name='beats',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
