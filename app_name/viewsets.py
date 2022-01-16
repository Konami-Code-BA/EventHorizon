from rest_framework import viewsets
from .serializers import UserSerializer, EventSerializer, ImageSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib import auth
from django.conf import settings
from decouple import config
from django.core.mail import send_mail
from app_name.functions import verify_update_line_info, authenticate_login, new_visitor, merge_email_into_line_account
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

	# PARTIAL_UPDATE ###############################################################################
	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
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

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		return Response()  # SECURITY: this just does nothing

	# CREATE #######################################################################################
	def create(self, request):  # POST {prefix}/
		user = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
		self.queryset = [user]
		if hasattr(self.queryset[0], 'error'):
			serializer_data = [OrderedDict([('error', self.queryset[0].error)])]
		else:
			serializer_data = self.serializer_class(self.queryset, many=True).data
		return Response(serializer_data)

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
		try:
			user = self.model.objects.get(pk=request.user.pk)  # get current user that made this request
			# if visitor made this request, remember that
			if user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
				visitor = request.user
		except self.model.DoesNotExist:  # if there is no currently existing user or visitor, make a new visitor
			user = new_visitor(request)
			request.user = user
		user = authenticate_login(request)  # it will try to login with email or line before loggin in by session
		if not hasattr(user, 'error'):  # if logged into a user
			user.visit_count += 1  # add to the visit count
			user.save()
			# if not visitor, but a visitor made the request
			if not user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists() and visitor:
				user.visit_count += visitor.visit_count
				user.save()
				visitor.delete()  # delete the visitor account that made the request
			return user  # done
		else:  # if couldn't login to anything, probably got an error, so return user anyway
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
			print('THE RESULT IS', result)
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
	def create(self, request):
		if request.user.is_superuser:  # SECURITY: only superuser can
			response = eval(f"self.{request.data['command']}(request)")  # SECURITY: inside each command function
			return Response(response)
		return Response('')

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
				postal_code, rand_latitude, rand_longitude = randomize_lat_lng(request.data['address'])
			else:
				latitude = 0
				longitude = 0
				postal_code, rand_latitude, rand_longitude = '', 0, 0
			event = self.model(
				name=request.data['name'],
				description=request.data['description'],
				address=request.data['address'],
				postal_code=postal_code,
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
			if 'images' in request.data:
				event.images.add(request.data['images'])
		try:
			serializer_data = self.serializer_class([event], many=True).data
		except Exception as e:
			print('ERROR IN ADD_EVENT API:', e)
			serializer_data = self.serializer_class([], many=True).data
		return serializer_data

	def my_events(self, request):  # SECURITY: anyone can get my events
		invited_events = self.model.objects.filter(invited=request.user.id)
		interested_public_events = self.model.objects.filter(Q(is_private=False) & Q(interested=request.user.id) & ~Q(invited=request.user.id))
		interested_private_events = self.model.objects.filter(Q(is_private=True) & Q(interested=request.user.id) & ~Q(invited=request.user.id))
		# SECURITY: freely gives invited_events and interested_public_events
		serializer_data1 = self.serializer_class(invited_events.union(interested_public_events), many=True).data
		# SECURITY: gives only limited info on interested_private_events 
		serializer_data2 = serializer_private(interested_private_events)
		return serializer_data1 + serializer_data2
	
	#def closest_future_date(self, request):
	#	date_time = request.data['date_time']
	#	invited_events = self.model.objects.filter(invited=request.user.id)
	#	print(date_time, type(date_time))

	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
		return Response()  # SECURITY: this just does nothing

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		my_events = self.model.objects.filter(invited=request.user.id) # gotta include public events
		event = self.model.objects.get(pk=pk)
		if event in my_events or not event.is_private:  # SECURITY: only get event if public or mine
			serializer_data = self.serializer_class([event], many=True).data
		else:
			serializer_data = serializer_private([event])
		return Response(serializer_data)

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		return Response()  # SECURITY: this just does nothing

	def list(self, request):  # GET {prefix}/
		my_events = self.model.objects.filter(invited=request.user.id)
		public_events = self.model.objects.filter(is_private=False)
		private_events = self.model.objects.filter(Q(is_private=True) & ~Q(invited=request.user.id))
		# SECURITY: freely gives my events and public events
		serializer_data1 = self.serializer_class(my_events.union(public_events), many=True).data
		# SECURITY: gives private events but i only get limited info on them
		serializer_data2 = serializer_private(private_events)
		return Response(serializer_data1 + serializer_data2)

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		return Response()  # SECURITY: this just does nothing


def randomize_lat_lng(address):
	gmaps = googlemaps.Client(key=config('GOOGLE_MAPS_API_KEY'))
	geocoded = gmaps.geocode(address)
	for component in geocoded[0]['address_components']:
		if 'postal_code' in component['types']:
			postal_code = component['long_name']
		if 'country' in component['types']:
			country = component['long_name']
	geocoded = gmaps.geocode(f'{postal_code} {country}')
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
	return postal_code, rand_latitude, rand_longitude


def serializer_private(events):
	serializer_data = []
	for event in events:
		serializer_data += [OrderedDict({
			'id': event.id,
			'name': event.name,
			'address': event.postal_code,
			'description': event.description,
			'latitude': event.rand_latitude,
			'longitude': event.rand_longitude,
			'date_time': event.date_time,
			'include_time': event.include_time,
			'is_private': event.is_private,
			'hosts': event.hosts.count(),
			'invited': event.invited.count(),
			'confirmed_guests': event.confirmed_guests.count(),
			'interested': event.interested.count(),
		})]
	return serializer_data


# IMAGES VIEW SET ######################################################################################################
class ImageViewset(viewsets.ViewSet):
	serializer_class = ImageSerializer
	model = serializer_class.Meta.model
	queryset = []

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

	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
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
