from rest_framework.response import Response
import requests, json, secrets
from decouple import config
from collections import namedtuple
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib import auth


def is_admin(request):  # is staff and is in the Admin group
	return request.user.is_staff and request.user.groups.filter(name='Admin').exists()


def is_admin_or_this_user(request, pk):  # is admin, or is a user that matches the pk
	return is_admin(request) or int(pk) == request.user.pk


def get_return_queryset(self, request, pk=None):
		if request.user.is_authenticated:  # is an authenticated user
				if pk:  # trying to access one user
						checker = is_admin_or_this_user(request, pk)  # check if is admin or is this user
				else:  # trying to access all users
						checker = is_admin(request)  # check if is admin
				objects = self.serializer_class.Meta.model.objects
				if checker:  # if accessing one user: is admin or is this user. if accessing all users, is admin
						if pk:  # trying to access one user
							try:
								queryset = objects.get(pk=pk)  # get the user
							except self.serializer_class.Meta.model.DoesNotExist:
								queryset = None
						else:  # trying to access all users
								queryset = objects.all()  # get all users
				else:  # is some user
						if pk:  # trying to access one other user
								queryset = None  # get nothing
						else:  # trying to access all users
								queryset = [request.user]  # get only himself
		else:  # unauthenticated user
				queryset = None  # get nothing
		if queryset:
			serializer_data = self.serializer_class(queryset, many=not bool(pk)).data
		else:
			serializer_data = None
		return Response(serializer_data)


def line_bot(line_body):
	replyToken, reply, received = None, None, None
	events = line_body['events'][0]
	if events['type'] == 'follow':
		reply = 'Thank you for following!'
		add_line_friend(events['source']['userId'])
	if events['type'] == 'unfollow':
		reply = 'Thank you for following!'
		remove_line_friend(events['source']['userId'])
	elif events['type'] == 'message':  # its a message (not a follow etc)
		if events['message']['type'] == 'text':  # its a text message (not an image etc)
			if events['message']['text'][:4] == '.bot':  # it has a .bot trigger
				received = events['message']['text'][5:]  # save the text minus the .bot trigger
			elif events['source']['type'] == 'user':  # it doesn't have a .bot trigger but it is a 1-user private room
				received = events['message']['text']  # private room doesn't need .bot trigger, so save all the text
	if 'replyToken' in events:
		replyToken = events['replyToken']
	if received in ['Status', 'status']:
		reply = '15 people confirmed'
	return replyToken, reply


def add_line_friend(line_id):
	from app_name.viewsets import UserViewset, SecretsViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		request = namedtuple('request', 'data')
		request.data = {'is_line_friend': True}
		UserViewset.update_user_is_line_friend(UserViewset, request, user.pk)  # update user, is_line_friend: True
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
		user.groups.add(5)  # temp line friend
		user.save()


def remove_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		request = namedtuple('request', 'data')
		request.data = {'is_line_friend': False}
		UserViewset.update_user_is_line_friend(UserViewset, request, user.pk)  # update user, is_line_friend: False
		user.do_get_lines = False
		user.save()
	except UserViewset.model.DoesNotExist:  # this is basically not possible
		pass


def authenticate_login(request):
	user = auth.authenticate(request)
	if user:
		user.save()
		auth.login(request, user)
	return user


def verify_update_line_info(request, user):  # for exisitng user with line id, access token already gotten
	print('step 7')
	visitor = None
	if request.user.groups.filter(id=3).exists():  # if visitor made this request to login by line
		print('step 8')
		visitor = type(user).objects.get(pk=request.user.pk)  # get visitor account making the request
	url = 'https://api.line.me/oauth2/v2.1/token'  # no matter if access token expired or not, refresh access token 1st
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	data = {
		'grant_type': 'refresh_token',
		'refresh_token': user.line_refresh_token,
		'client_id': config('LOGIN_CHANNEL_ID'),
		'client_secret': config('LOGIN_CHANNEL_SECRET'),
	}
	print('step 9')
	refreshAccessToken_response = json.loads(requests.post(url, headers=headers, data=data).content)
	print('step 10')
	# if refresh token is expired, this is session login attempt, block attempt and force them to click the line
	# login button and do a line login from the start
	if 'error' in refreshAccessToken_response:
		print('step 11')
		return None
	user.line_access_token = refreshAccessToken_response['access_token']  # save new access token to user data
	user.line_refresh_token = refreshAccessToken_response['refresh_token']  # also refresh token
	url = 'https://api.line.me/oauth2/v2.1/verify?access_token=' + user.line_access_token  # first verify access token
	print('step 12')
	verify_response = json.loads(requests.get(url).content)
	print('step 13')
	if verify_response['client_id'] != config('LOGIN_CHANNEL_ID'):  # make sure verification not intercepted
		print('step 14')
		return None  # client id can't be confirmed
	url = 'https://api.line.me/v2/profile'  # get line profile info
	headers = {'Authorization': 'Bearer ' + user.line_access_token}
	print('step 15')
	profile_response = json.loads(requests.get(url, headers=headers).content)
	print('step 16')
	if user.do_get_line_display_name:  # update display name with line profile name unless user set not to
		user.display_name = profile_response['displayName']
	if profile_response['userId'] == user.line_id:  # double check line id is correct and this wasnt somehow faked
		print('step 17')
		user.save()
		request.data['line_id'] = user.line_id
		print('step 18', user.__dict__)
		user = authenticate_login(request)  # login again just in case, and to get new location info
		print('step 19', user.__dict__)
		if user:  # logged into a user
			print('step 20')
			if not user.groups.filter(id=3).exists() and visitor:  # if not visitor, but request made by visitor
				visitor.delete()  # delete the visitor account that made the request
				print('DELETED VISITOR')
		return user
	else:  # line id can't be confirmed
		print('step 21')
		return None


def new_visitor(request):
	from app_name.viewsets import UserViewset, SecretsViewset
	print('ENTER NEW VISITOR')
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
	request.data['random_secret'] = user.random_secret
	auth.login(request, user)
	return user
