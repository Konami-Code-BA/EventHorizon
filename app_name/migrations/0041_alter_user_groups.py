# Generated by Django 3.2.3 on 2021-07-15 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app_name', '0040_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, to='auth.Group'),
        ),
    ]