from rest_framework import viewsets, filters
from .models import User, Alert
from .serializers import UserSerializer
from rest_framework.response import Response
from django.contrib import auth
from django.conf import settings
from decouple import config
from django.core.mail import send_mail
from app_name.functions import get_return_queryset, verify_update_line_info, authenticate_login, new_visitor
from django.http import HttpResponse
import secrets, requests, json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class UserViewset(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = serializer_class.Meta.model.objects.all()
	model = User

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
		return user
	
	def update_user_do_get_emails(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.do_get_emails = request.data['do_get_emails']
		user.save()
		return user
	
	def update_user_is_line_friend(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		user.is_line_friend = request.data['is_line_friend']
		user.save()
		return user
	
	def update_user_alerts(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			return None
		alert = Alert.objects.get(name=request.data['name'])
		if user.alerts.filter(name=request.data['name']).exists():  # if user has this alert, remove it
			alert.user_set.remove(user)
		else:  # if user does not have this alert, add it
			alert.user_set.add(user)
		return user

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		return get_return_queryset(self, request, pk=pk)

	# CREATE ###########################################################################################################
	def create(self, request):  # POST {prefix}/
		user = eval(f"self.{request.data['command']}(request)")
		if user:
			request.user = user
		return get_return_queryset(self, request, pk=request.user.pk)

	def register_with_email(self, request):
		if ('email' in request.data and 'password' in request.data and 'display_name' in request.data and
				request.data['email'] != '' and request.data['password'] != '' and request.data['display_name'] != ''):
			try:  # check this email hasn't already been registered
				user = self.model.objects.get(email=request.data['email'])
				user = None  # if already registered, don't let them register another name wtih existing email
			except self.model.DoesNotExist:  # if this email not already registered, turn visitor into user & add info
				user = self.model.objects.get(pk=request.user.pk)  # get visitor account (already logged in)
				user.groups.clear()  # clear visitor group
				user.groups.add(2)  # change to user
				print('CHANGED VISITOR')
				user.display_name = request.data['display_name']  # add new user account info
				user.email = request.data['email']
				user.password = make_password(request.data['password'])
				user.do_get_emails = True
				user.is_superuser = False
				user.is_staff = False
				user.save()
				user = authenticate_login(request)  # login user
			return user
		else:
			return None

	def line_new_device(self, request):
		print('step1')
		if config('PYTHON_ENV', default='production') == 'development':  # get url depending on dev or prod
			uri = 'http://127.0.0.1:8080/loginRegister'
		else:
			uri = 'https://www.eventhorizon.vip/loginRegister'
		url = 'https://api.line.me/oauth2/v2.1/token'  # use code to get access token
		data = {
			'grant_type': 'authorization_code',
			'code': request.data['code'],
			'redirect_uri': uri,
			'client_id': config('LOGIN_CHANNEL_ID'),
			'client_secret': config('LOGIN_CHANNEL_SECRET'),
		}
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		print('step2')
		getAccessToken_response = json.loads(requests.post(url, headers=headers, data=data).content)
		print('step3')
		url = 'https://api.line.me/v2/profile'  # use access token to get profile info
		headers = {'Authorization': 'Bearer ' + getAccessToken_response['access_token']}
		print('step4')
		profile_response = json.loads(requests.get(url, headers=headers).content)
		print('step5')
		try:  # try to get a user with this user id, if there is one then set all the new data to their account
			print('step6')
			user = User.objects.get(line_id=profile_response['userId'])
			user = verify_update_line_info(request, user)  # verify validity of current line data and put new data
		except User.DoesNotExist:  # if there was no user with this id, turn visitor into user & add info
			print('step 22')
			user = self.model.objects.get(pk=request.user.pk)  # get visitor account (already logged in)
			print('step 23')
			user.groups.clear()  # clear visitor group
			user.groups.add(2)  # change to user
			print('CHANGED VISITOR')
			user.display_name = profile_response['displayName']  # add new user account info
			user.line_id = profile_response['userId']
			user.line_access_token = getAccessToken_response['access_token']
			user.line_refresh_token = getAccessToken_response['refresh_token']
			user.do_get_lines = True
			user.do_get_line_display_name = True
			print('step 24', user.__dict__)
			user.save()
			print('step 25', user.__dict__)
			user = authenticate_login(request)  # login user
			print('step 26', user.__dict__)
		print('step 27')
		return user
		

	def login(self, request):
		#return authenticate_login(request)  # FOR EMERGENCY LOGIN
		visitor = None
		if request.user.groups.filter(id=3).exists():  # if visitor made this request
			visitor = self.model.objects.get(pk=request.user.pk)  # get current visitor
		user = authenticate_login(request)  # it will try to login with email or line before session
		if user:  # if logged into a user
			if not user.groups.filter(id=3).exists() and visitor:  # if not visitor, but a visitor made the request
				visitor.delete()  # delete the visitor account that made the request
				print('DELETED VISITOR')
			return user  # done
		else:  # if couldn't log into a user, not even a visitor, make a new visitor
			user = new_visitor(request)
			request.user = user
			user = authenticate_login(request)  # login user
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
		url = 'https://api.line.me/v2/bot/message/quota/consumption'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		response = requests.get(url, headers=headers)
		return response

	def broadcast(self, request):
		url = 'https://api.line.me/v2/bot/message/broadcast'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = json.dumps({
			'messages': [{
				"type": "text",
				"text": request.data['message'],
			}]
		})
		response = requests.post(url, headers=headers, data=data)
		return response

	def push(self, request):
		mikeyOrStu = {
			'mikey': config('MIKEY_LINE_USER_ID'),
			'stu': config('STU_LINE_USER_ID'),
		},
		url = 'https://api.line.me/v2/bot/message/push'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = json.dumps({
			'to': mikeyOrStu[request.data['to']],
			'messages': [{
				"type": "text",
				"text": request.data['message'],
			}]
		})
		response = requests.post(url, headers=headers, data=data)
		return response


class SecretsViewset(viewsets.ViewSet):
	queryset = []
	secrets_dict = {
		'random_secret': secrets.token_urlsafe(16),
		'login_channel_id': config('LOGIN_CHANNEL_ID'),
	}
	def retrieve(self, request, pk=None):
		print('getting secret', pk)
		print('result is', self.secrets_dict[pk])
		return HttpResponse(self.secrets_dict[pk])


class AlertViewset(viewsets.ViewSet):
	queryset = []
	secrets_dict = {
		'random_secret': secrets.token_urlsafe(16),
		'login_channel_id': config('LOGIN_CHANNEL_ID'),
	}
	def retrieve(self, request, pk=None):
		return HttpResponse(self.secrets_dict[pk])
