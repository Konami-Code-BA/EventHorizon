from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
	use_in_migrations = True

	def create_user(self, username, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		print('create_user 1')
		if not username:
			raise ValueError('The given username must be set')
		print('create_user 2')
		email = self.normalize_email(email)
		print('create_user 3')
		# Lookup the real model class from the global app registry so this
		# manager method can be used in migrations. This is fine because
		# managers are by definition working on the real model.
		GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
		print('create_user 4')
		username = GlobalUserModel.normalize_username(username)
		print('create_user 5')
		user = self.model(username=username, email=email, **extra_fields)
		print('create_user 6')
		user.password = make_password(password)
		print('create_user 7')
		print('self', self)
		print('self._db', self._db)
		#user.save(using=self._db)
		user.save()
		print('create_user 8')
		return user


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
	username = models.CharField(max_length=40, default='', unique=False, blank=True)

	objects = UserManager()


class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('id',)
	list_display = ('display_name', 'email', 'line_id', 'pk')
	fields = (
		'id', 'display_name', 'email', 'do_get_emails', 'line_id', 'line_access_token', 'line_refresh_token',
		'do_get_line_display_name', 'is_line_friend', 'do_get_lines', 'language', 'groups', 'user_permissions',
		'is_staff', 'is_superuser', 'last_login', 'date_joined', 'ip_continent_name', 'ip_country_name',
		'ip_state_prov', 'ip_city',
	)
