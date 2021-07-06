from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.conf import settings


class User(AbstractUser):
	display_name = models.CharField(max_length=40, default='', blank=False)
	language = models.CharField(max_length=2, default='EN', blank=False)
	do_get_emails = models.BooleanField(default=False, blank=False)
	line_id = models.CharField(max_length=40, default='', blank=True)
	line_access_token = models.CharField(max_length=300, default='', blank=True)
	line_refresh_token = models.CharField(max_length=40, default='', blank=True)
	do_get_line_display_name = models.BooleanField(default=True, blank=False)
	is_line_friend = models.BooleanField(default=False, blank=False)
	do_get_lines = models.BooleanField(default=False, blank=False)
	random_secret = models.CharField(max_length=40, default='', blank=True)
	ip_continent_name = models.CharField(max_length=40, default='', blank=True)
	ip_country_name = models.CharField(max_length=40, default='', blank=True)
	ip_state_prov = models.CharField(max_length=40, default='', blank=True)
	ip_city = models.CharField(max_length=40, default='', blank=True)
	ip_date = models.CharField(max_length=40, default='', blank=True)



class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)
	list_display = ('display_name', 'email', 'line_id', 'pk')
	fields = (
		'id', 'display_name', 'email', 'do_get_emails', 'line_id', 'line_access_token', 'line_refresh_token',
		'do_get_line_display_name', 'is_line_friend', 'do_get_lines', 'language', 'groups', 'user_permissions',
		'is_staff', 'is_superuser', 'last_login', 'date_joined', 'ip_continent_name', 'ip_country_name',
		'ip_state_prov', 'ip_city',
	)
