# Generated by Django 3.0.8 on 2020-07-21 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_videoobj'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videoobj',
            old_name='name',
            new_name='title',
        ),
    ]
