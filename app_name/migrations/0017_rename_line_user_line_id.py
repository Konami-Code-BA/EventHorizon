# Generated by Django 3.2.3 on 2021-07-04 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0016_delete_line'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='line',
            new_name='line_id',
        ),
    ]