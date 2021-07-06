# Generated by Django 3.2.3 on 2021-07-02 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0010_user_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='line_state',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='get_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='get_line',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='line',
            field=models.CharField(default='', max_length=40),
        ),
    ]
