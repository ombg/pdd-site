# Generated by Django 3.0.8 on 2020-07-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_pdd'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdd',
            name='videos',
            field=models.ManyToManyField(to='core.VideoObj'),
        ),
    ]
