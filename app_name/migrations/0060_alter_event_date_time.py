# Generated by Django 4.0 on 2021-12-26 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0059_alter_event_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 26, 20, 52, 30, 508791)),
        ),
    ]
