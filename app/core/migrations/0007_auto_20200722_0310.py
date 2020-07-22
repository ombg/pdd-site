# Generated by Django 3.0.8 on 2020-07-22 03:10

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_videoobj_videofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoobj',
            name='videofile',
        ),
        migrations.AddField(
            model_name='pdd',
            name='videofile',
            field=models.FileField(null=True, upload_to=core.models.pddobj_video_file_path),
        ),
    ]
