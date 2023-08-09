from django.db import migrations
from django.contrib.auth.models import Group


def create_groups(apps, schema_editor):
    groups = ['Admin', 'User', 'Temp Line Friend']
    for group in groups:
        Group.objects.create(name=group)


class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(create_groups),
    ]
