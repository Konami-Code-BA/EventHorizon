from rest_framework import viewsets, filters, permissions
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.conf import settings
from django.contrib.sessions.models import Session
from decouple import config
from django.core.mail import send_mail
from app_name.functions import get_return_queryset, api_to_line, new_user_from_request
from django.http import HttpResponse
import secrets


class UserViewset(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = serializer_class.Meta.model.objects.all()
	model = User
	filter_backends = (filters.SearchFilter,)
	search_fields = ['=email', '=username',]

	def list(self, request):  # GET {prefix}/
		return get_return_queryset(self, request)

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		return get_return_queryset(self, request, pk=pk)

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		return get_return_queryset(self, request, pk=pk)

	# PARTIAL_UPDATE ###################################################################################################
	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
		user = eval(f"self.{request.data['command']}(request, pk)")
		return get_return_queryset(self, request, pk=pk)
	
	def update_user_language(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.language = request.data['language']
		user.save()
	
	def update_user_do_get_emails(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.do_get_emails = request.data['do_get_emails']
		user.save()
	
	def update_user_is_line_friend(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.is_line_friend = request.data['is_line_friend']
		user.save()
	
	def update_user_location(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.ip_continent_name = request.data['ip_continent_name']
		user.ip_country_name = request.data['ip_country_name']
		user.ip_state_prov = request.data['ip_state_prov']
		user.ip_city = request.data['ip_city']
		user.ip_date = request.data['ip_date']
		user.save()

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		return get_return_queryset(self, request, pk=pk)

	# CREATE ###########################################################################################################
	def create(self, request):  # POST {prefix}/
		user = eval(f"self.{request.data['command']}(request)")
		return get_return_queryset(self, request, pk=request.user.pk)

	def register_by_email(self, request):
		user = new_user_from_request(request)
		self.login(request)
		print('REGISTERED AND LOGGED IN')
		return user

	#def register_by_line(self, request):
	#	display_name = request.data['display_name']
	#	line = request.data['line_id']
	#	line_access_token = request.data['line_access_token']
	#	get_line = True
	#	language = request.data['language']
	#	user = User.objects.create_user(
	#		display_name=display_name, line=line, line_access_token=line_access_token, get_line=get_line,
	#		language=language,
	#	)
	#	user.save()
	#	group = Group.objects.get(name='User')
	#	group.user_set.add(user)
	#	self.login(self, request)
	#	return user

	def login(self, request):
		user = auth.authenticate(request)
		if user:
			auth.login(request, user)
		return user

	def logout(self, request):
		try:
			user = self.model.objects.get(pk=request.user.pk)
			auth.logout(request)
			return user
		except self.model.DoesNotExist:
			return
	
	def send_email(self, request):
		subject = 'Test sending email from site from mikey'
		message = 'Was I able to send it?'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['mdsimeone@gmail.com',]
		send_mail(subject, message, email_from, recipient_list, fail_silently=False)


class LineViewset(viewsets.ViewSet):
	queryset = []
	def create(self, request):
		response = eval(f"self.{request.data['command']}(request)")
		return Response(response)

	def consumption(self, request):
		response = api_to_line('consumption')
		return response

	def broadcast(self, request):
		response = api_to_line('broadcast', message=request.data['message'])
		return response

	def push(self, request):
		mikeyOrStu = {
			'mikey': config('MIKEY_LINE_USER_ID'),
			'stu': config('STU_LINE_USER_ID'),
		},
		towho = mikeyOrStu[request.data['to']]
		response = api_to_line('push', message=request.data['message'], towho=towho)
		return response

	def new_device(self, request):
		language = request.data['language']
		if config('PYTHON_ENV', default='production') == 'development':
			uri = 'http://127.0.0.1:8080/loginRegister'
		else:
			uri = 'https://www.eventhorizon.vip/loginRegister'
		params = {
			'grant_type': 'authorization_code',
			'code': request.data['code'],
			'redirect_uri': uri,
			'client_id': config('LOGIN_CHANNEL_ID'),
			'client_secret': config('LOGIN_CHANNEL_SECRET'),
		}
		response =  api_to_line('getAccessToken', params=params)
		line_access_token = response['access_token']
		line_refresh_token = response['refresh_token']
		params = {
			'access_token': line_access_token,
		}
		response = api_to_line('profile', params=params)
		line_id = response['userId']
		display_name = response['displayName']
		random_secret = SecretsViewset.retrieve(SecretsViewset, None, 'random_secret')
		try:
			user = User.objects.get(line_id=line_id)
			user.line_access_token = line_access_token
			user.line_refresh_token = line_refresh_token
			user.language = language
			user.random_secret = random_secret
			if user.do_get_line_display_name:
				user.display_name = display_name
			user.save()
			request.data['line_id'] = line_id
			request.user = user
		except User.DoesNotExist:
			user = User.objects.create_user(
				display_name=display_name, line_id=line_id, line_access_token=line_access_token, do_get_lines=True,
				username='USER', language=language, is_superuser=False, is_staff=False, random_secret=random_secret,
			)
			user.save()
			group = Group.objects.get(name='User')
			group.user_set.add(user)
			request.data['line_id'] = line_id
			request.user = user
		UserViewset.login(UserViewset, request)
		
	def verify(self, request):
		user = User.objects.get(pk=request.user.pk)
		params = {
			'access_token': user.line_access_token,
		}
		response = api_to_line('verify', params=params)
		if response['client_id']==config('LOGIN_CHANNEL_ID') and response['expires_in'] > 0:
			response = self.profile(request)
		elif request.data['expires_in'] <= 0:
			1

	#def profile(self, request):
	#	user = User.objects.get(pk=request.user.pk)
	#	params = {
	#		'access_token': user.line_access_token,
	#	}
	#	if request.data['client_id'] == config('LOGIN_CHANNEL_ID') and request.data['expires_in'] > 0:
	#		response = api_to_line('profile', params=params)
	#	elif request.data['expires_in'] <= 0:
	#		# TODO need to do refresh of access token
	#		response = None
	#	return response


class SecretsViewset(viewsets.ViewSet):
	queryset = []
	secrets_dict = {
		'random_secret': secrets.token_urlsafe(16),
		'login_channel_id': config('LOGIN_CHANNEL_ID'),
	}
	def retrieve(self, request, pk=None):
		return HttpResponse(self.secrets_dict[pk])
