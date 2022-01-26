from rest_framework import viewsets
from .serializers import UserSerializer, EventSerializer, ImageSerializer, PlusOneSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib import auth
from django.conf import settings
from decouple import config
from django.core.mail import send_mail
from app_name.functions import verify_update_line_info, authenticate_login, new_visitor, merge_email_into_line_account
from app_name.functions import user_in_guest_statuses
import secrets, requests, json
from django.contrib.auth.hashers import make_password
from collections import namedtuple, OrderedDict
from django.db.models import Q
import googlemaps
import random
import boto3
from botocore.exceptions import ClientError
import io
from datetime import datetime
import base64


random.seed(1)


## gotta make sure all of these are secure for every API
#def list(self, request):  # GET {prefix}/
#	pass
#def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
#	pass
#def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
#	pass
#def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
#	pass
#def create(self, request):  # POST {prefix}/
#	pass
#def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
#	pass

# USER VIEW SET ########################################################################################################
class UserViewset(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	model = serializer_class.Meta.model
	queryset = model.objects.all()

	def list(self, request):  # GET {prefix}/
		self.queryset = [request.user]  # SECURITY: list only returns yourself
		serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		self.queryset = [request.user]  # SECURITY: retrieve only returns yourself
		serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		self.queryset = [request.user]  # SECURITY: update only returns yourself
		serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		return Response()  # SECURITY: this just does nothing

	# PARTIAL_UPDATE #############################################################
	def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
		user = eval(f"self.{request.data['command']}(request, pk)")  # SECURITY: inside each command function
		self.queryset = [user]
		if hasattr(self.queryset[0], 'error'):
			serializer_data = [OrderedDict([('error', self.queryset[0].error)])]
		else:
			serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)
	
	def update_user_language(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
			return user
		if user == request.user:  # SECURITY: you can only do this for yourself
			user.language = request.data['language']
			user.save()
			return user
		else:
			user = namedtuple('user', 'error')
			user.error = 'you don\'t have permission'
			return user
	
	def update_user_do_get_emails(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
			return user
		if user == request.user:  # SECURITY: you can only do this for yourself
			user.do_get_emails = request.data['do_get_emails']
			user.save()
			return user
		else:
			user = namedtuple('user', 'error')
			user.error = 'you don\'t have permission'
			return user
	
	def update_user_do_get_lines(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
			return user
		if user == request.user:  # SECURITY: you can only do this for yourself
			user.do_get_lines = request.data['do_get_lines']
			user.save()
			return user
		else:
			user = namedtuple('user', 'error')
			user.error = 'you don\'t have permission'
			return user
	
	#def update_user_alerts(self, request, pk):
	#	try:
	#		user = self.model.objects.get(pk=pk)
	#	except self.model.DoesNotExist:
	#		user = namedtuple('user', 'error')
	#		user.error = 'a user with this id could not be found'
	#		return user
	#	alert = Alert.objects.get(name=request.data['name'])
	#	if user.alerts.filter(name=request.data['name']).exists():  # if user has this alert, remove it
	#		alert.user_set.remove(user)
	#	else:  # if user does not have this alert, add it
	#		alert.user_set.add(user)
	#	return user
	
	def register_email(self, request, pk):
		if ('email' in request.data and 'password' in request.data and request.data['email'] != '' and
				request.data['password'] != ''):
			try:  # get the current user
				current_user = self.model.objects.get(pk=pk)
				if current_user != request.user:  # SECURITY: you can only do this for yourself
					user = namedtuple('user', 'error')
					user.error = 'you don\'t have permission'
					return user
				# if user is visitor, should be in register_with_email
				if current_user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
					user = namedtuple('user', 'error')
					user.error = 'something strange happened... a visitor should not be able to run this'
					return user
			except self.model.DoesNotExist:  # if can't get current user
				user = namedtuple('user', 'error')
				user.error = 'a user with this id could not be found'
				return user
			try:  # check if a user with the new email exists
				existing_user = self.model.objects.get(email=request.data['email'])
				# if existing user with this email does exist, check their password, and if its good too, merge accounts
				if existing_user.check_password(request.data['password']):  # if password matches too
					current_user = merge_email_into_line_account(current_user, existing_user)  # merge accounts
					return current_user
				else:  # if password doesn't match
					user = namedtuple('user', 'error')
					user.error = 'Incorrect password for this email'
					return user
			except self.model.DoesNotExist:  # if exisiting user with this email doesnt exist, add email to current user
				current_user.email = request.data['email']
				current_user.password = make_password(request.data['password'])
				current_user.do_get_emails = True
				current_user.save()
				return current_user
		else:  # missing email / password info
			user = namedtuple('user', 'error')
			user.error = 'missing email / password info'
			return user
	
	def message_user(self, request, pk):
		try:
			user = self.model.objects.get(pk=pk)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
			return user
		event = EventSerializer.Meta.model.objects.get(pk=request.data['event_id'])
		# SECURITY: i must be the host of the event id im passing, and the user must be affiliated with that event
		# note: before we let people make events. people could make an event and invite someone just to be able to message them. this could be an issue later.
		if user_in_guest_statuses(event, request.user.id, ['hosts']) and user_in_guest_statuses(
				event, pk, ['hosts', 'invited', 'wait_list', 'invite_request']):
			if user.do_get_lines:
				data = {"to": user.line_id, "messages": [{"type": "text", "text": request.data['message']}]}
				url = 'https://api.line.me/v2/bot/message/push'
				headers = {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
				}
				data = json.dumps(data)
				response = requests.post(url, headers=headers, data=data)
			if user.do_get_emails:
				subject = 'Event Horizon Notification'
				message = request.data['message']
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email,]
				send_mail(subject, message, email_from, recipient_list, fail_silently=False)
			return request.user
		else:
			user = namedtuple('user', 'error')
			user.error = 'you don\'t have permission'
			return user

	# CREATE #####################################################################
	def create(self, request):  # POST {prefix}/
		user = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
		self.queryset = [user]
		if hasattr(self.queryset[0], 'error'):
			serializer_data = [OrderedDict([('error', self.queryset[0].error)])]
		elif type(user) != self.model:
			serializer_data = user
		else:
			serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)

	#def get_user_limited_info(self, request):  # SECURITY: retrieve only returns id/pk and name of user
	#	user_array = self.model.objects.filter(pk__in=request.data['ids'])
	#	serializer_data = []
	#	for all_user_info_dont_send_me in user_array:
	#		serializer_data += [OrderedDict([
	#			('id', all_user_info_dont_send_me.id),
	#			('pk', all_user_info_dont_send_me.pk),
	#			('display_name', all_user_info_dont_send_me.display_name),
	#			('limited_user', True),
	#			('plus_ones', []),
	#		])]
	#	return serializer_data

	def get_event_user_info(self, request):  # SECURITY: retrieve only returns display_name of user
		# everyone can see hosts
		# can't see invited/attending/maybe people if not invited
		# can't see wait_list, invite_request people if not host
		event = EventSerializer.Meta.model.objects.get(pk=request.data['event_id'])
		plus_ones = event.plus_ones.all()
		guest_ids = getattr(event, request.data['guest_type']).all().values_list('id', flat=True)
		actual_guest_array = list(self.model.objects.filter(pk__in=guest_ids))
		final_guest_array = []
		for guest in actual_guest_array:
			# if it is me, i get more info. also if i am a host
			if guest.id == request.user.id or user_in_guest_statuses(event, request.user.id, ['hosts']):
				final_guest_array += [OrderedDict([
					('id', guest.id),
					('display_name', guest.display_name),
					('limited_user', True),
					('plus_one', False),
				])]
				if request.data['guest_type'] != 'hosts':  # hosts' plus-ones aren't added to hosts, they're added elsewhere
					plus_one = plus_ones.filter(chaperone=guest.id)  # get plus-one for this guest
					if len(plus_one) > 0:  # if there is a plus-one
						final_guest_array += [OrderedDict([
							('id', guest.id),
							('display_name', plus_one[0].name),
							('limited_user', True),
							('plus_one', True),
						])]
			elif ((  # get some info if
					request.user.id in event.invited.all().values_list('id', flat=True)  # im invited and
					and request.data['guest_type'] in ['invited', 'attending', 'maybe']  # get invited/attending/maybe
				) or (  # or im getting hosts
					request.data['guest_type'] == 'hosts'
				)
			):
				final_guest_array += [OrderedDict([
					('display_name', guest.display_name),
					('limited_user', True),
					('plus_one', False),
				])]
				if request.data['guest_type'] != 'hosts':  # hosts' plus-ones aren't added to hosts, they're added elsewhere
					plus_one = plus_ones.filter(chaperone=guest.id)  # get plus-one for this guest
					if len(plus_one) > 0:  # if there is a plus-one
						final_guest_array += [OrderedDict([
							('display_name', plus_one[0].name),
							('limited_user', True),
							('plus_one', True),
						])]
			else: # im not getting me, im not a host, im not invited getting invitees, im not getting hosts
				final_guest_array += [OrderedDict([
					('limited_user', True),
					('plus_one', False),
				])]
				if request.data['guest_type'] != 'hosts':  # hosts' plus-ones aren't added to hosts, they're added elsewhere
					plus_one = plus_ones.filter(chaperone=guest.id)  # get plus-one for this guest
					if len(plus_one) > 0:  # if there is a plus-one
						final_guest_array += [OrderedDict([
							('limited_user', True),
							('plus_one', True),
						])]
		return final_guest_array
	
	def message_users(self, request):
		for id in request.data['user_ids']:
			try:
				user = self.model.objects.get(pk=id)
			except self.model.DoesNotExist:
				user = namedtuple('user', 'error')
				user.error = 'a user with this id could not be found'
				continue
			event = EventSerializer.Meta.model.objects.get(pk=request.data['event_id'])
			# SECURITY: i must be the host of the event id im passing, and the user must be affiliated with that event
			# note: before we let people make events. people could make an event and invite someone just to be able to message them. this could be an issue later.
			if user_in_guest_statuses(event, request.user.id, ['hosts']) and user_in_guest_statuses(
					event, id, ['hosts', 'invited', 'wait_list', 'invite_request']):
				if user.do_get_lines:
					data = {"to": user.line_id, "messages": [{"type": "text", "text": request.data['message']}]}
					url = 'https://api.line.me/v2/bot/message/push'
					headers = {
						'Content-Type': 'application/json',
						'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
					}
					data = json.dumps(data)
					response = requests.post(url, headers=headers, data=data)
				if user.do_get_emails:
					subject = 'Event Horizon Notification'
					message = request.data['message']
					email_from = settings.EMAIL_HOST_USER
					recipient_list = [user.email,]
					send_mail(subject, message, email_from, recipient_list, fail_silently=False)
				continue
			else:
				user = namedtuple('user', 'error')
				user.error = 'you don\'t have permission'
				continue

	def register_with_email(self, request):  # SECURITY: anyone is allowed to make a new user
		if ('email' in request.data and 'password' in request.data and 'display_name' in request.data and
				request.data['email'] != '' and request.data['password'] != '' and request.data['display_name'] != ''):
			try:  # check this email hasn't already been registered
				# if already registered, don't let them register another name with existing email
				user = self.model.objects.get(email=request.data['email'])
				user = namedtuple('user', 'error')
				user.error = 'This email is already registered'
			except self.model.DoesNotExist:  # if this email not already registered, turn visitor into user & add info
				user = self.model.objects.get(pk=request.user.pk)  # get visitor account (already logged in)
				user.groups.clear()  # clear visitor group
				user.groups.add(Group.objects.get(name='User').id)  # change to user
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
			user = namedtuple('user', 'error')
			user.error = 'email / password / display name are missing or empty'
			return user

	def line_new_device(self, request):  # SECURITY: anyone is allowed to make a new line device
		if config('PYTHON_ENV', default='\'"production"\'') == 'development':  # get url depending on dev, test, or prod
			uri = 'http://127.0.0.1:8080' + request.data['path']
		elif config('PYTHON_ENV', default='\'"production"\'') == '\'"test"\'':
			uri = 'https://event-horizon-test.herokuapp.com' + request.data['path']
		else:
			uri = 'https://www.eventhorizon.vip' + request.data['path']
		url = 'https://api.line.me/oauth2/v2.1/token'  # use code to get access token
		data = {
			'grant_type': 'authorization_code',
			'code': request.data['code'],
			'redirect_uri': uri,
			'client_id': config('LOGIN_CHANNEL_ID'),
			'client_secret': config('LOGIN_CHANNEL_SECRET'),
		}
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		getAccessToken_response = json.loads(requests.post(url, headers=headers, data=data).content)
		if 'error' in getAccessToken_response:
			user = namedtuple('user', 'error')
			user.error = getAccessToken_response['error_description']
			return user
		url = 'https://api.line.me/v2/profile'  # use access token to get profile info
		headers = {'Authorization': 'Bearer ' + getAccessToken_response['access_token']}
		profile_response = json.loads(requests.get(url, headers=headers).content)
		try:  # try to get a user with this line id, if there is one then set all the new data to their account
			user = self.model.objects.get(line_id=profile_response['userId'])
			user.line_access_token = getAccessToken_response['access_token']
			user.line_refresh_token = getAccessToken_response['refresh_token']
			user.do_get_lines = True
			# if this user is a temp line friend
			if user.groups.filter(id=Group.objects.get(name='Temp Line Friend').id).exists():
				user.groups.clear()  # clear temp line friend group
				user.groups.add(Group.objects.get(name='User').id)  # change to user
			print('CHANGING TEMP LINE FRIEND TO USER')
			user = verify_update_line_info(request, user)  # verify validity of current line data and put new data
		except self.model.DoesNotExist:  # if there was no user with this id, add line info to existing account
			user = self.model.objects.get(pk=request.user.pk)  # get account (already logged in)
			if user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():  # if visitor
				user.groups.clear()  # clear visitor group
				user.groups.add(Group.objects.get(name='User').id)  # change to user
			user.display_name = profile_response['displayName']  # add new user account info
			user.line_id = profile_response['userId']
			user.line_access_token = getAccessToken_response['access_token']
			user.line_refresh_token = getAccessToken_response['refresh_token']
			user.do_get_line_display_name = True
			user.do_get_lines = True
			user.save()
			print('SAVED USER')
			user = authenticate_login(request)  # login user
			print('LOGGED IN')
		return user

	def login(self, request):  # SECURITY: anyone is allowed to login
		#return authenticate_login(request)  # FOR EMERGENCY LOGIN (also in backends)
		visitor = False
		print('START***************************************************')
		try:
			user = self.model.objects.get(pk=request.user.pk)  # get current user that made this request
			# if visitor made this request, remember that
			if user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
				visitor = request.user
			print('1***************************************************')
		except self.model.DoesNotExist:  # if there is no currently existing user or visitor, make a new visitor
			user = new_visitor(request)
			request.user = user
			print('2***************************************************')
		user = authenticate_login(request)  # it will try to login with email or line before loggin in by session
		print('3***************************************************')
		if not hasattr(user, 'error'):  # if logged into a user
			print('4***************************************************')
			user.visit_count += 1  # add to the visit count
			print('4b***************************************************')
			user.save()
			print('4c***************************************************')
			# if not visitor, but a visitor made the request
			if not user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists() and visitor:
				print('5***************************************************')
				user.visit_count += visitor.visit_count
				user.save()
				visitor.delete()  # delete the visitor account that made the request
			print('6***************************************************')
			print(user)
			return user  # done
		else:  # if couldn't login to anything, probably got an error, so return user anyway
			print('7***************************************************')
			print(user)
			return user

	def logout(self, request):  # SECURITY: anyone is allowed to logout
		try:
			user = self.model.objects.get(pk=request.user.pk)
			auth.logout(request)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
		return user
	
	def send_email(self, request):
		subject = 'Test sending email from site from mikey'
		message = 'Was I able to send it?'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['mdsimeone@gmail.com',]
		send_mail(subject, message, email_from, recipient_list, fail_silently=False)
		return self.model.objects.get(pk=request.user.pk)
	
	def forgot_password(self, request):
		try:
			user = self.model.objects.get(email=request.data['email'])
			user.random_secret = secrets.token_urlsafe(16)
			user.save()
			subject = 'Event Horizon - Change Password Link'
			message = f'Please follow this link to change your password:\n'
			message += request.data['return_link'] + '&code=' + user.random_secret
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [request.data['email'],]
			result = send_mail(subject, message, email_from, recipient_list, fail_silently=False)
			user = self.model.objects.get(pk=request.user.pk)
		except self.model.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'This email is not registered'
		return user
		
	def change_password(self, request):
		current_user = self.model.objects.get(pk=request.user.pk)
		user = self.model.objects.get(email=request.data['email'])
		if ((
			'code' in request.data and user.random_secret == request.data['code']
		) or (
			'current_password' in request.data and user.check_password(request.data['current_password'])
		)):
			user.password = make_password(request.data['new_password'])
			user.random_secret = ''
			user.save()
			if current_user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
				current_user.delete()
			user = authenticate_login(request)  # login user
		else:
			user = namedtuple('user', 'error')
			user.error = 'wrong code or password'
		return user


# LINE VIEW SET ########################################################################################################
class LineViewset(viewsets.ViewSet):
	queryset = []

	def list(self, request):  # GET {prefix}/
		pass

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		pass

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		pass

	def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
		pass

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		pass

	def create(self, request):
		if request.user.is_superuser:  # SECURITY: only superuser can
			response = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
		else:
			response = {}
			response['error'] = 'only superuser can do this'
		return Response(response)

	def consumption(self, request):  # SECURITY: messaging channel access token only used here in backend
		url = 'https://api.line.me/v2/bot/message/quota/consumption'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		response = requests.get(url, headers=headers)
		return response

	def broadcast(self, request):  # SECURITY: messaging channel access token only used here in backend
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

	def push(self, request):  # SECURITY: messaging channel access token only used here in backend
		mikeyOrStu = {
			'mikey': config('MIKEY_LINE_USER_ID'),
			'stu': config('STU_LINE_USER_ID'),
		}
		data = request.data['data']
		data['to'] = mikeyOrStu[data['to']]
		url = 'https://api.line.me/v2/bot/message/push'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = json.dumps(data)
		response = requests.post(url, headers=headers, data=data)
		return response


# SECRETS VIEW SET #####################################################################################################
class SecretsViewset(viewsets.ViewSet):
	queryset = []
	
	def list(self, request):  # GET {prefix}/
		pass
	
	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		pass

	def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
		pass

	def create(self, request):  # POST {prefix}/
		pass

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		pass

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		if ((pk in ['mikey-line-user-id', 'stu-line-user-id'] and request.user.is_superuser)
				or pk not in ['mikey-line-user-id', 'stu-line-user-id']):  # SECURITY: only superuser can get our ids
			secrets_dict = {
				'new-random-secret': secrets.token_urlsafe(16),
				# SECURITY: this is safe because of domain restriction, and channel secret not used in client, only back
				'login-channel-id': config('LOGIN_CHANNEL_ID'),
				# SECURITY: this is safe because of domain restriction
				'google-maps-api-key': config('GOOGLE_MAPS_API_KEY'),
				# SECURITY: this is safe because only superuser can get it
				'mikey-line-user-id': config('MIKEY_LINE_USER_ID'),
				# SECURITY: this is safe because only superuser can get it
				'stu-line-user-id': config('STU_LINE_USER_ID'),
			}
			return Response(secrets_dict[pk])
		return Response()


# EVENTS VIEW SET ######################################################################################################
class EventViewset(viewsets.ViewSet):
	serializer_class = EventSerializer
	model = serializer_class.Meta.model
	queryset = []

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		pass

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		pass

	# CREATE #####################################################################
	def create(self, request):  # POST {prefix}/
		response = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
		return Response(response)

	def add_event(self, request):
		event = None
		if request.user.is_superuser:  # SECURITY: only superuser can add event
			if request.data['address']:
				gmaps = googlemaps.Client(key=config('GOOGLE_MAPS_API_KEY'))
				geocoded = gmaps.geocode(request.data['address'])
				latitude = geocoded[0]['geometry']['location']['lat']
				longitude = geocoded[0]['geometry']['location']['lng']
				address, area, rand_latitude, rand_longitude = randomize_lat_lng(request.data['address'])
			else:
				latitude = 0
				longitude = 0
				address, area, rand_latitude, rand_longitude = '', '', 0, 0
			event = self.model(
				name=request.data['name'],
				description=request.data['description'],
				address=address,
				area=area,
				venue_name=request.data['venue_name'],
				latitude=latitude,
				longitude=longitude,
				rand_latitude=rand_latitude,
				rand_longitude=rand_longitude,
				date_time=request.data['date_time'],
				include_time=request.data['include_time'],
				is_private=request.data['is_private'],
			)
			event.save()
			event.hosts.add(request.user.id)
			event.invited.add(request.user.id)
			event.maybe.add(request.user.id)
			if 'images' in request.data:
				event.images.add(request.data['images'])
		try:
			serializer_data = self.serializer_class([event], many=True).data
		except Exception as e:
			print('ERROR IN ADD_EVENT API:', e)
			serializer_data = self.serializer_class([], many=True).data
		return serializer_data

	def my_events(self, request):  # SECURITY: anyone can get my events
		my_hosting = self.model.objects.filter(hosts=request.user.id)
		serializer_data_my_hosting = serializer_host(my_hosting)  # SECURITY: see serializers
		my_invited = self.model.objects.filter(Q(invited=request.user.id) & ~Q(hosts=request.user.id))
		serializer_data_my_invited = serializer_public_invited(my_invited)
		my_invite_requests = self.model.objects.filter(Q(is_private=True) & Q(invite_request=request.user.id))
		serializer_data_my_invite_requests = serializer_private(my_invite_requests)
		return serializer_data_my_hosting + serializer_data_my_invited + serializer_data_my_invite_requests

	#def closest_future_date(self, request):
	#	date_time = request.data['date_time']
	#	invited_events = self.model.objects.filter(invited=request.user.id)
	#	print(date_time, type(date_time))

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		my_hosting = self.model.objects.filter(hosts=request.user.id)
		my_invited = self.model.objects.filter(Q(invited=request.user.id) & ~Q(hosts=request.user.id))
		event = self.model.objects.get(pk=pk)
		if event in my_hosting:
			serializer_data = serializer_host([event])  # SECURITY: see serializers
		elif event in my_invited or not event.is_private:
			serializer_data = serializer_public_invited([event])
		else:
			serializer_data = serializer_private([event])
		return Response(serializer_data)

	def list(self, request):  # GET {prefix}/
		my_hosting = self.model.objects.filter(
			hosts=request.user.id
		)
		serializer_data_my_hosting = serializer_host(my_hosting)  # SECURITY: see serializers
		my_invited = self.model.objects.filter(
			Q(invited=request.user.id) & ~Q(hosts=request.user.id)
		)
		serializer_data_my_invited = serializer_public_invited(my_invited)
		public_events = self.model.objects.filter(
			Q(is_private=False) & ~Q(invited=request.user.id) & ~Q(hosts=request.user.id)
		)
		serializer_data_public_events = serializer_public_invited(public_events)
		private_events = self.model.objects.filter(
			Q(is_private=True) & ~Q(invited=request.user.id) & ~Q(hosts=request.user.id)
		)
		serializer_data_private_events = serializer_private(private_events)
		return Response(
			serializer_data_my_hosting
			+ serializer_data_my_invited
			+ serializer_data_public_events
			+ serializer_data_private_events
		)

	# PARTIAL_UPDATE #############################################################
	def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
		eval(f"self.{request.data['command']}(request, pk)")  # SECURITY: inside each command function
		return Response()  # SECURITY: returns nothing
	
	def update_guest_status(self, request, pk):
		event = self.model.objects.get(pk=pk)  # SECURITY: in the following comments
		if event.hosts.filter(id=request.user.id).exists():  # only host can change other users statuses
			if request.data['user_id']:
				user_to_change = request.data['user_id']
			else:
				user_to_change = request.user.id
		else:  # non host can only change his own status
			user_to_change = request.user.id
		if request.data['status'] == 'decline':  # anyone can decline
			event.invited.remove(user_to_change)
			event.maybe.remove(user_to_change)
			event.attending.remove(user_to_change)
			event.wait_list.remove(user_to_change)
			event.invite_request.remove(user_to_change)
			plus_one = event.plus_ones.filter(chaperone=request.user.id)
			plus_one.delete()
		elif request.data['status'] == 'invite_request':
			if not request.user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
				event.invite_request.add(user_to_change)  # only non-visitors can request an invite
		#elif request.data['status'] == 'invited':
		#	if event.hosts.filter(id=request.user.id).exists():  # only host can invite user if private
		#		event.invited.add(user_to_change)
		#		event.maybe.add(user_to_change)
		elif request.data['status'] == 'wait_list':
			# only invited can be changed to wait_list (unless its public)
			if event.invited.filter(id=user_to_change).exists() or not event.is_private:
				event.attending.remove(user_to_change)
				event.maybe.remove(user_to_change)
				event.invited.remove(user_to_change)
				event.invited.add(user_to_change)
				event.wait_list.add(user_to_change)
		elif request.data['status'] == 'maybe':
			# only invited can be changed to maybe (unless its public)
			if event.invited.filter(id=user_to_change).exists() or not event.is_private:
				event.attending.remove(user_to_change)
				event.wait_list.remove(user_to_change)
				event.invited.remove(user_to_change)
				event.invited.add(user_to_change)
				event.maybe.add(user_to_change)
		elif request.data['status'] == 'attending':
			# only invited can be changed to maybe (unless its public)
			if event.invited.filter(id=user_to_change).exists() or not event.is_private:
				plus_one = event.plus_ones.filter(chaperone=request.user.id)
				addition = 1 + len(plus_one)
				if len(event.attending.all()) + addition <= event.attending_limit:  # can't join attending if no space
					event.maybe.remove(user_to_change)
					event.wait_list.remove(user_to_change)
					event.invited.remove(user_to_change)
					event.invited.add(user_to_change)
					event.attending.add(user_to_change)
				else:
					return [OrderedDict([('error', 'full')])]
		return {}  # SECURITY: returns nothing


def randomize_lat_lng(address):
	gmaps = googlemaps.Client(key=config('GOOGLE_MAPS_API_KEY'))
	geocoded = gmaps.geocode(address)
	address = geocoded[0]['formatted_address']
	area = ''
	for component in geocoded[0]['address_components']:
		if 'sublocality_level_2' in component['types']:
			area += component['long_name']
		if 'locality' in component['types']:
			area += ', ' + component['long_name']
		if 'postal_code' in component['types']:
			area += ' ' + component['long_name']
		if 'country' in component['types']:
			country = component['long_name']
	geocoded = gmaps.geocode(f'{area} {country}')
	outter = 300
	latitude = geocoded[0]['geometry']['location']['lat']
	rand_sign = 1 if random.random() > .5 else -1
	rand_value = random.random()
	rand_latitude = float(latitude) + rand_value / outter * rand_sign
	outter = 350
	longitude = geocoded[0]['geometry']['location']['lng']
	rand_sign = 1 if random.random() > .5 else -1
	rand_value = random.random()
	rand_longitude = float(longitude) + rand_value / outter * rand_sign
	return address, area, rand_latitude, rand_longitude

# SECURITY:
# address only shows area if not invited
# no venu_name if not invited
# random lat and long if not invited
# everyone can see hosts and images
# can't see invited/attending/ maybe people if not invited
# can't see wait_list, invite_request people if not host
def serializer_private(events):
	serializer_data = []
	for event in events:
		serializer_data += [OrderedDict({
			'id': event.id,
			'name': event.name,
			'address': event.area,
			'description': event.description,
			'latitude': event.rand_latitude,
			'longitude': event.rand_longitude,
			'date_time': event.date_time,
			'include_time': event.include_time,
			'is_private': event.is_private,
			'hosts': event.hosts.all().values_list('id', flat=True),
			'invited': event.invited.count(),
			'attending': event.attending.count(),
			'maybe': event.maybe.count(),
			'wait_list': event.wait_list.count(),
			'invite_request': event.invite_request.count(),
			'images': event.images.all().values_list('id', flat=True),
			'attending_limit': event.attending_limit,
		})]
	return serializer_data


def serializer_public_invited(events):
	serializer_data = []
	for event in events:
		serializer_data += [OrderedDict({
			'id': event.id,
			'name': event.name,
			'address': event.address,
			'venue_name': event.venue_name,
			'description': event.description,
			'latitude': event.latitude,
			'longitude': event.longitude,
			'date_time': event.date_time,
			'include_time': event.include_time,
			'is_private': event.is_private,
			'hosts': event.hosts.all().values_list('id', flat=True),
			'invited': event.invited.all().values_list('id', flat=True),
			'attending': event.attending.all().values_list('id', flat=True),
			'maybe': event.maybe.all().values_list('id', flat=True),
			'wait_list': event.wait_list.count(),
			'invite_request': event.invite_request.count(),
			'images': event.images.all().values_list('id', flat=True),
			'attending_limit': event.attending_limit,
		})]
	return serializer_data


def serializer_host(events):
	serializer_data = []
	for event in events:
		serializer_data += [OrderedDict({
			'id': event.id,
			'name': event.name,
			'address': event.address,
			'venue_name': event.venue_name,
			'description': event.description,
			'latitude': event.latitude,
			'longitude': event.longitude,
			'date_time': event.date_time,
			'include_time': event.include_time,
			'is_private': event.is_private,
			'hosts': event.hosts.all().values_list('id', flat=True),
			'invited': event.invited.all().values_list('id', flat=True),
			'attending': event.attending.all().values_list('id', flat=True),
			'maybe': event.maybe.all().values_list('id', flat=True),
			'wait_list': event.wait_list.all().values_list('id', flat=True),
			'invite_request': event.invite_request.all().values_list('id', flat=True),
			'images': event.images.all().values_list('id', flat=True),
			'attending_limit': event.attending_limit,
		})]
	return serializer_data


# IMAGES VIEW SET ######################################################################################################
class ImageViewset(viewsets.ViewSet):
	serializer_class = ImageSerializer
	model = serializer_class.Meta.model
	queryset = []

	def list(self, request):  # GET {prefix}/
		pass

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		pass

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		pass

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		pass

	def create(self, request):  # POST {prefix}/ 
		if request.data['command'] == 'get':
			result = []
			for key in request.data['keys'].split(','):
				if 'MapIcon' in key:
					result += aws_get_file(key)
				else: 
					result += {'error': 'Not authorized'}
			response = HttpResponse(result)
			response['Content-Type'] = "image/png"
			response['Cache-Control'] = "max-age=0"
			return response
		else:  # create
			file = request.data['file']
			result = aws_upload_file(file)
			if 'error' in result:
				serializer_data = self.serializer_class([result], many=True).data
			else:
				image = self.model(key=result['key'])
				image.save()
				serializer_data = self.serializer_class([image], many=True).data
			return Response(serializer_data)

	def partial_update(self, request, pk):  # PATCH {prefix}/{lookup}/
		if request.data['command'] == 'get':
			my_events = EventSerializer.Meta.model.objects.filter(invited=request.user.id)
			event = EventSerializer.Meta.model.objects.get(pk=request.data['event_pk'])
			image = self.model.objects.get(pk=pk)
			if image in event.images.all() and event in my_events:
				result = aws_get_file(image.key)
				response = HttpResponse(result)
				response['Content-Type'] = "image/jpg"
				response['Cache-Control'] = "max-age=0"
				return response
			else:
				serializer_data = self.serializer_class([{'error': 'Not authorized'}], many=True).data
			return Response(serializer_data)
		else:
			serializer_data = self.serializer_class([{'error': 'Not get command'}], many=True).data
			return Response(serializer_data)

def aws_upload_file(file):
	s3_client = boto3.client(
		's3',
		aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
		aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
	)
	try:
		file_type = '.' + file.name.split('.')[len(file.name.split('.'))-1]
		if file_type not in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', '.gif', '.PNG']:
			return {'error': 'Not supported file type'}
		key = str(datetime.now()).replace(' ', 'T').replace(':', '_').replace('.', '_')
		key += '--' + str(secrets.token_urlsafe(4)) + file_type
		s3_client.upload_fileobj(file, config('AWS_BUCKET_ACCESS_POINT'), key)
		return {'key': key}
	except ClientError as e:
		print('AWS S3 UPLOAD ERROR:', e)
		return {'error': e}

def aws_get_file(key):
	try:
		s3_client = boto3.client(
			's3',
			aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
		)
		file_stream = io.BytesIO()
		s3_client.download_fileobj(config('AWS_BUCKET_ACCESS_POINT'), key, file_stream)
		send = base64.b64encode(file_stream.getbuffer())
		return send
	except ClientError as e:
		print('AWS S3 UPLOAD ERROR:', e)
		return {'error': e}


# PLUS ONE VIEW SET ######################################################################################################
class PlusOneViewset(viewsets.ViewSet):
	serializer_class = PlusOneSerializer
	model = serializer_class.Meta.model
	queryset = []
	
	# everyone can see hosts
	# can't see invited/attending/maybe plus ones if not invited
	# can't see wait_list/invite_request plus ones if not host
	def list(self, request):  # GET {prefix}/
		pass  # SECURITY: does nothing

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		pass  # SECURITY: does nothing

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		pass  # SECURITY: does nothing

	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
		pass  # SECURITY: does nothing

	def create(self, request):  # POST {prefix}/
		result = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
		return Response(result)

	def set_plus_one(self, request):  # get is done in get_event_user_info
		event = EventSerializer.Meta.model.objects.get(pk=request.data['event_id'])
		if event.plus_ones.filter(chaperone=request.user.id).exists():  # SECURITY: user can't add more than 1 plus-one
			return [OrderedDict([('error', 'user can\'t add more than 1 plus-one')])]
		if (  # SECURITY:  only someone part of this event (in any way) can add a plus-one
			event.hosts.filter(id=request.user.id).exists()
			or event.invited.filter(id=request.user.id).exists()
			or event.attending.filter(id=request.user.id).exists()
			or event.maybe.filter(id=request.user.id).exists()
			or event.wait_list.filter(id=request.user.id).exists()
			or event.invite_request.filter(id=request.user.id).exists()
		):
			plus_one = self.model(name='(+1) ' + request.data['plus_one_name'])
			plus_one.save()
			plus_one.chaperone.add(request.user.id)
			event.plus_ones.add(plus_one.id)
			return [OrderedDict([('success', plus_one.id)])]
		else:
			return [OrderedDict([('error', 'you are not affiliated with this event')])]

	def delete_plus_one(self, request):
		event = EventSerializer.Meta.model.objects.get(pk=request.data['event_id'])
		if not event.plus_ones.filter(chaperone=request.user.id).exists():  # SECURITY: can't del +1 if doesnt exist
			return [OrderedDict([('error', 'user can\'t add more than 1 plus-one')])]
		if (  # SECURITY:  only someone part of this event (in any way) can delete a plus-one
			event.hosts.filter(id=request.user.id).exists()
			or event.invited.filter(id=request.user.id).exists()
			or event.attending.filter(id=request.user.id).exists()
			or event.maybe.filter(id=request.user.id).exists()
			or event.wait_list.filter(id=request.user.id).exists()
			or event.invite_request.filter(id=request.user.id).exists()
		):
			plus_one = event.plus_ones.filter(chaperone=request.user.id)
			plus_one.delete()
			return []
		else:
			return [OrderedDict([('error', 'you are not affiliated with this event')])]

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		pass  # SECURITY: does nothing
