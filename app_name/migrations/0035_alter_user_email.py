# Generated by Django 3.2.3 on 2021-07-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0034_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]