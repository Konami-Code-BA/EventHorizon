# Generated by Django 3.2.3 on 2021-07-13 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0037_auto_20210713_2115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='alert_name',
            new_name='name',
        ),
    ]