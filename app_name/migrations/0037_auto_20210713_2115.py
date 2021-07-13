# Generated by Django 3.2.3 on 2021-07-13 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0036_auto_20210713_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='cookies',
            new_name='show',
        ),
        migrations.AddField(
            model_name='alert',
            name='alert_name',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
    ]
