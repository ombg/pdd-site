# Generated by Django 3.0.8 on 2020-07-22 01:10

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_pdd_videos'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoobj',
            name='videofile',
            field=models.FileField(null=True, upload_to=core.models.pddobj_video_file_path),
        ),
    ]
