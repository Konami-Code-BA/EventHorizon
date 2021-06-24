from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.conf import settings


class User(AbstractUser):
		language = models.CharField(max_length=2, default='EN')
		getEmails = models.BooleanField(default=True)

class Line(models.Model):
    response = models.CharField(max_length=400)

class UserAdmin(admin.ModelAdmin):
		list_display = ('username', 'email', 'first_name', 'last_name', 'pk', 'is_staff')
