from rest_framework.response import Response
import requests, json


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
								queryset = objects.get(pk=pk)  # get the user
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
		print('serializer_data:', serializer_data)
		return Response(serializer_data)


def line_bot(line_body):
	replyToken, reply, received = None, None, None
	events = line_body['events'][0]
	if events['type'] == 'follow':
		reply = 'Thank you for following!'
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


def api_to_line(todo, message=None, towho=None):
	token = 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU='
	urls = {
		'push': 'https://api.line.me/v2/bot/message/push',
		'reply': 'https://api.line.me/v2/bot/message/reply',
		'multicast': 'https://api.line.me/v2/bot/message/multicast',
		'broadcast': 'https://api.line.me/v2/bot/message/broadcast',
		'consumption': 'https://api.line.me/v2/bot/message/quota/consumption',
	}
	send_type = {
		'push': 'to',
		'reply': 'replyToken',
		'multicast': 'to',
		'broadcast': None,
		'consumption': None,
	}
	headers = {
		'Content-Type': 'application/json',
		'Authorization': 'Bearer ' + token,
	}
	if message:  # if there's a message, want to send the message, its a post
		data = {}
		if towho:  # if there is a towho, put it in the data, otherwise it's a broadcast to all
			data[send_type[todo]] = towho
		data['messages'] = [{
			"type": "text",
			"text": message,
		}]
		response = requests.post(  # post it
			urls[todo],
			headers = headers,
			data = json.dumps(data)
		)
	else:  # if there's no message, it's a get
		response = requests.get(  # get it
			urls[todo],
			headers = headers
		)
	return json.loads(response.content)


#def line_push(message):
#	token = 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU='
	#response = requests.post(
	#	'https://api.line.me/v2/bot/message/push',
	#	headers = {
	#		'Content-Type': 'application/json',
	#		'Authorization': 'Bearer ' + token,
	#	},
	#	data = json.dumps({
	#		"to": 'U09e3b108910c1711d2732a8b9ac8a19d',
	#		"messages": [
	#			{
	#				"type": "text",
	#				"text": message,
	#			}
	#		]
	#	})
	#)
	#return response


#def line_reply(replyToken, message):
#	print('inside line reply')
#	token = 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU='
#	response = requests.post(
#		'https://api.line.me/v2/bot/message/reply',
#		headers = {
#			'Content-Type': 'application/json',
#			'Authorization': 'Bearer ' + token,
#		},
#		data = json.dumps({
#			"replyToken": replyToken,
#			"messages": [
#				{
#					"type": "text",
#					"text": message,
#				}
#			]
#		})
#	)
#	return response
