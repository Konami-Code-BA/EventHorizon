# Generated by Django 3.2.3 on 2021-07-04 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0019_alter_user_line_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
    ]
