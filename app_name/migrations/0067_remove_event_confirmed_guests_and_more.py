# Generated by Django 4.0 on 2022-01-18 13:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0066_alter_event_address_alter_event_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='confirmed_guests',
        ),
        migrations.RemoveField(
            model_name='event',
            name='interested',
        ),
        migrations.AddField(
            model_name='event',
            name='attending',
            field=models.ManyToManyField(blank=True, related_name='attending', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='invite_request',
            field=models.ManyToManyField(blank=True, related_name='invite_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='maybe',
            field=models.ManyToManyField(blank=True, related_name='maybe', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='wait_list',
            field=models.ManyToManyField(blank=True, related_name='wait_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
