# Generated by Django 3.2.3 on 2021-06-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0006_user_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='getEmails',
            field=models.BooleanField(default=True),
        ),
    ]