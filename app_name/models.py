from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Line(models.Model):
    response = models.CharField(max_length=400)
