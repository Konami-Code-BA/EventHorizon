# Generated by Django 3.2.3 on 2021-07-04 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0021_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='do_get_line_display_name',
            field=models.BooleanField(default=True),
        ),
    ]
