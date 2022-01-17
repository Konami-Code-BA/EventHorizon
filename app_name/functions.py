from rest_framework.response import Response
import requests, json, secrets
from decouple import config
from collections import namedtuple, OrderedDict
from django.contrib.auth.models import Group
from django.contrib import auth
from .models import Alert


def is_admin(request):  # is staff and is in the Admin group
	return request.user.is_staff and request.user.groups.filter(name='Admin').exists()


def is_admin_or_this_user(request, pk):  # is admin, or is a user that matches the pk
	return is_admin(request) or int(pk) == request.user.pk


# this doesnt work anymore, also im not sure how necessary it is. keeping it for now tho in case i want it later
#def get_return_queryset(self, request, pk=None):
#	if hasattr(request.user, 'error'):  # not a user, just an error
#		queryset = [request.user]
#	elif request.user.is_authenticated:  # is an authenticated user
#		if pk:  # trying to access one user
#			checker = is_admin_or_this_user(request, pk)  # check if is admin or is this user
#		else:  # trying to access all users
#			checker = is_admin(request)  # check if is admin
#		objects = self.serializer_class.Meta.model.objects
#		if checker:  # if accessing one user: is admin or is this user. if accessing all users, is admin
#			if pk:  # trying to access one user
#				try:
#					queryset = [objects.get(pk=pk)]  # get the user
#				except self.serializer_class.Meta.model.DoesNotExist:
#					user = namedtuple('user', 'error')
#					user.error = 'a user with this id could not be found'
#					queryset = [user]
#			else:  # trying to access all users
#				queryset = objects.all()  # get all users
#		else:  # is some user
#			if pk:  # trying to access one other user
#				user = namedtuple('user', 'error')
#				user.error = 'you don\'t have permission to access other users'
#				queryset = [user]
#			else:  # trying to access all users
#				queryset = [request.user]  # get only himself
#	else:  # unauthenticated user
#		user = namedtuple('user', 'error')
#		user.error = 'you are not an authenticated user'
#		queryset = [user]
#	if hasattr(queryset[0], 'error'):
#		serializer_data = [OrderedDict([('error', queryset[0].error)])]
#	else:
#		serializer_data = self.serializer_class(queryset, many=True).data
#	return Response(serializer_data)


def line_bot(line_body):
	replyToken, reply, received = None, None, None
	if len(line_body['events']) > 0:
		events = line_body['events'][0]
	else: 
		return replyToken, reply
	if events['type'] == 'follow':
		reply = {'type': 'text', 'text': 'Thank you for following!'}
		add_line_friend(events['source']['userId'])
	if events['type'] == 'unfollow':
		remove_line_friend(events['source']['userId'])
	elif events['type'] == 'message':  # its a message (not a follow etc)
		if events['message']['type'] == 'text':  # its a text message (not an image etc)
			if events['message']['text'][0] == '.':  # it has a bot trigger
				received = events['message']['text'][1:]  # save the text minus the bot trigger
			elif events['source']['type'] == 'user':  # it doesn't have a bot trigger but it is a 1-user private room
				received = events['message']['text']  # private room doesn't need bot trigger, so save all the text
	if 'replyToken' in events:
		send_to = {'type': 'replyToken', 'to': events['replyToken']}
	if 'to' in events:
		send_to = {'type': 'to', 'to': events['to']}
	if received and ('status' in received or 'Status' in received):
		reply = {'type': 'text', 'text': 'Here is your status brah'}
	elif received and ('image' in received or 'Image' in received):
		reply = {'type': 'image', 'image': 'Here is your image brah'}  # need to send an image file not text here.
	return send_to, reply


def add_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		user.is_line_friend = True
		user.do_get_lines = True
		user.save()
		print('CHANGED is_line_friend AND do_get_lines FOR EXISTING LINE FRIEND')
	except UserViewset.model.DoesNotExist:  # if no user with this line id exists
		# this wasn't done on the site, it was done in line so there is no visitor, and can't make session
		user = UserViewset.model.objects.create_user(  # create temporary line friend user
			line_id = line_id,
			do_get_lines = True,
			is_line_friend = True,
			display_name = 'Temp Line Friend', 
			do_get_line_display_name = True,
			random_secret = secrets.token_urlsafe(16)
		)
		user.groups.add(Group.objects.get(name='Temp Line Friend').id)  # temp line friend
		user.save()
		print('ADDED NEW TEMP LINE FRIEND')


def remove_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		user.is_line_friend = False
		user.do_get_lines = False
		user.save()
	except UserViewset.model.DoesNotExist:  # this is basically not possible
		pass


def authenticate_login(request):
	user = auth.authenticate(request)
	if not hasattr(user, 'error'):
		user.save()
		auth.login(request, user)
	return user


def verify_update_line_info(request, user):  # for exisitng user with line id, access token already gotten
	visitor = None
	# if visitor made this request to login by line
	if request.user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists():
		visitor = type(user).objects.get(pk=request.user.pk)  # get visitor account making the request
	url = 'https://api.line.me/oauth2/v2.1/token'  # no matter if access token expired or not, refresh access token 1st
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	data = {
		'grant_type': 'refresh_token',
		'refresh_token': user.line_refresh_token,
		'client_id': config('LOGIN_CHANNEL_ID'),
		'client_secret': config('LOGIN_CHANNEL_SECRET'),
	}
	refreshAccessToken_response = json.loads(requests.post(url, headers=headers, data=data).content)
	# if refresh token is expired, this is session login attempt, block attempt and force them to click the line
	# login button and do a line login from the start
	if 'error' in refreshAccessToken_response:
		user = namedtuple('user', 'error')
		user.error = refreshAccessToken_response['error_description']
		return user
	user.line_access_token = refreshAccessToken_response['access_token']  # save new access token to user data
	user.line_refresh_token = refreshAccessToken_response['refresh_token']  # also refresh token
	url = 'https://api.line.me/oauth2/v2.1/verify?access_token=' + user.line_access_token  # first verify access token
	verify_response = json.loads(requests.get(url).content)
	if verify_response['client_id'] != config('LOGIN_CHANNEL_ID'):  # make sure verification not intercepted
		user = namedtuple('user', 'error')
		user.error = 'could not verify client id when trying to verify access token'
		return user  # client id can't be confirmed
	url = 'https://api.line.me/v2/profile'  # get line profile info
	headers = {'Authorization': 'Bearer ' + user.line_access_token}
	profile_response = json.loads(requests.get(url, headers=headers).content)
	if user.do_get_line_display_name:  # update display name with line profile name unless user set not to
		user.display_name = profile_response['displayName']
	if profile_response['userId'] == user.line_id:  # double check line id is correct and this wasnt somehow faked
		user.save()
		request.data['line_id'] = user.line_id
		user = authenticate_login(request)  # login again just in case, and to get new location info
		if not hasattr(user, 'error'):  # logged into a user
			# if not visitor, but request made by visitor
			if not user.groups.filter(id=Group.objects.get(name='Temp Visitor').id).exists() and visitor:
				user.visit_count += visitor.visit_count
				user.save()
				visitor.delete()  # delete the visitor account that made the request
		return user
	else:  # line id can't be confirmed
		user = namedtuple('user', 'error')
		user.error = 'could not verify line id after getting line profile info'
		return user


def new_visitor(request):
	from app_name.viewsets import UserViewset, SecretsViewset
	for i in range(1000):
		random_secret = secrets.token_urlsafe(16)
		try:
			user = UserViewset.model.objects.get(random_secret=random_secret)
		except UserViewset.model.MultipleObjectsReturned:
			pass
		except UserViewset.model.DoesNotExist:
			break
	user = UserViewset.model.objects.create_user(
		random_secret = random_secret,
		display_name = 'Visitor',
	)
	user.save()
	group = Group.objects.get(id=3)
	group.user_set.add(user)
	alert = Alert.objects.get(name='Show Cookies')
	alert.user_set.add(user)
	request.data['random_secret'] = user.random_secret
	auth.login(request, user)
	return user


def merge_email_into_line_account(current_user, existing_user):
	current_user.password = existing_user.password
	# last_login remains current_user's
	current_user.email = existing_user.email
	# is_active remains current_user's (true)
	if existing_user.date_joined < current_user.date_joined:
		current_user.date_joined = existing_user.date_joined
	# display_name remains current_user's
	# language remains current_user's
	current_user.do_get_emails = True
	# all line things remain current user's
	# random_secret remains current_user's
	current_user.visit_count += existing_user.visit_count
	current_user.save()
	existing_user.delete()
	return current_user
