# Generated by Django 3.2.3 on 2021-06-18 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0004_alter_user_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created_by',
        ),
    ]