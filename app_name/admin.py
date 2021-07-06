from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import User, UserAdmin


admin.site.register(User, UserAdmin)
