# Generated by Django 4.0 on 2022-01-20 08:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0069_rename_plusones_plusone'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='plus_ones',
            field=models.ManyToManyField(blank=True, related_name='plus_ones', to=settings.AUTH_USER_MODEL),
        ),
    ]