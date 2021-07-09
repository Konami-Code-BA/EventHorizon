from rest_framework.response import Response
import requests, json
from decouple import config
from collections import namedtuple
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


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
		add_temp_line_friend(events['source']['userId'])
	if events['type'] == 'unfollow':
		reply = 'Thank you for following!'
		remove_temp_line_friend(events['source']['userId'])
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


def api_to_line(todo, message=None, towho=None, params=None):
	channel_access_token = config('MESSAGING_CHANNEL_ACCESS_TOKEN')
	urls = {
		'push': 'https://api.line.me/v2/bot/message/push',
		'reply': 'https://api.line.me/v2/bot/message/reply',
		'multicast': 'https://api.line.me/v2/bot/message/multicast',
		'broadcast': 'https://api.line.me/v2/bot/message/broadcast',
		'consumption': 'https://api.line.me/v2/bot/message/quota/consumption',
		'getAccessToken': 'https://api.line.me/oauth2/v2.1/token',
		'verify': 'https://api.line.me/oauth2/v2.1/verify?access_token=',
		'profile': 'https://api.line.me/v2/profile',
	}
	send_type = {
		'push': 'to',
		'reply': 'replyToken',
		'multicast': 'to',
		'broadcast': None,
		'consumption': None,
	}
	headers = {}
	data = None
	if params:  # if there are params, it's for getAccessToken, verify, or profile
		if todo == 'getAccessToken':
			headers['Content-Type'] = 'application/x-www-form-urlencoded'
			data = params
		elif todo == 'profile':
			headers['Authorization'] = 'Bearer ' + params['access_token']
		elif todo == 'verify':
			urls[todo] = urls[todo] + params['access_token']
	else:  # if no params, it's for consumption or one of the message ones
		headers['Content-Type'] = 'application/json'
		headers['Authorization'] = 'Bearer ' + channel_access_token
		if message:  # if there's a message, want to send the message
			data = {}
			if towho:  # if there is a towho, put it in the data, otherwise it's a broadcast to all
				data[send_type[todo]] = towho
			data['messages'] = [{
				"type": "text",
				"text": message,
			}]
			data = json.dumps(data)
	
	if data:  # requests with data
		if headers == {}:  # requests with no headers
			response = requests.post(  # post it
				urls[todo],
				data = data,
			)
		else:  # requests with headers
			response = requests.post(  # post it
				urls[todo],
				headers = headers,
				data = data,
			)
	else:  # requests with no data
		if headers == {}:  # requests with no headers
			response = requests.get(  # get it
				urls[todo],
			)
		else:  # requests with headers
			response = requests.get(  # get it
				urls[todo],
				headers = headers,
			)
	
	return json.loads(response.content)


def add_temp_line_friend(line_id):
	from app_name.viewsets import UserViewset, SecretsViewset
	try:
		user = UserViewset.model.objects.get(line_id=line_id)
		request = namedtuple('request', 'data')
		request.data = {'is_line_friend': True}
		UserViewset.update_user_is_line_friend(UserViewset, request, user.pk)
	except UserViewset.model.DoesNotExist:
		random_secret = SecretsViewset.retrieve(SecretsViewset, None, 'random_secret')
		user = UserViewset.model.objects.create_user(
			line_id=line_id, do_get_lines=True, username='USER', is_superuser=False, is_staff=False,
			is_line_friend=True, display_name='TEMP', random_secret=random_secret,
		)
		user.save()


def remove_temp_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:
		user = UserViewset.model.objects.get(line_id=line_id)
		request = namedtuple('request', 'data')
		request.data = {'is_line_friend': False}
		UserViewset.update_user_is_line_friend(UserViewset, request, user.pk)
	except UserViewset.model.DoesNotExist:
		pass


def new_user_from_request(request):
	from app_name.viewsets import UserViewset, SecretsViewset
	display_name = request.data['display_name']
	language = request.data['language']
	if 'email' in request.data and 'password' in request.data:
		email = request.data['email']
		password = request.data['password']
		random_secret = SecretsViewset.retrieve(SecretsViewset, None, 'random_secret').content.decode("utf-8")
		user = UserViewset.model.objects.create_user(display_name=display_name, email=email,
			password=make_password(password), do_get_emails=True, do_get_line_display_name=True, language=language,
			is_superuser=False, is_staff=False, random_secret=random_secret)
		group = Group.objects.get(name='User')
		group.user_set.add(user)
