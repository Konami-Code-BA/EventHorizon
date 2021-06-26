# Generated by Django 3.2.3 on 2021-06-18 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0003_alter_user_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]