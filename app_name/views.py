from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
import json
import requests
from app_name.viewsets import UserViewSet, LineViewset
from app_name.functions import line_bot, api_to_line
	
def index(request):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def line_webhook(request):
	line_body = json.loads(request.body.decode('utf-8'))
	print('line_body', line_body)
	received_message_1 = {  # https://developers.line.biz/en/reference/messaging-api/#message-event
		'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
		'events': [
			{
				'type': 'message',
				'message': {
					'type': 'text',
					'id': '14296801432826',
					'text': 'status'
				},
				'timestamp': 1624799029188,
				'source': {
					'type': 'user',
					'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
				},
				'replyToken': '3ef6d67db3304eebab8588ce2eff6331',
				'mode': 'active'
			}
		]
	}
	received_message_2 = {
		'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
		'events': [{
			'type': 'message',
			'message': {
				'type': 'text',
				'id': '14302576500342',
				'text': '.bot status'
			},
			'timestamp': 1624886647207,
			'source': {
				'type': 'room',
				'roomId': 'R243cbfb03168e95081d5895c2f99a4b5',
				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
			},
			'replyToken': 'c16418c3cc2a4aab82ab961a024f2ea8',
			'mode': 'active'
		}]
	}
	new_follower_1 = {
		'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
		'events': [{
			'type': 'follow',
			'timestamp': 1624799586678,
			'source': {
				'type': 'user',
				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
			},
			'replyToken': 'be6008d01ab84e1a8ee7699102927f00',
			'mode': 'active'
		}]
	}
	lost_follower_1 = {
		'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
		'events': [{
			'type': 'unfollow',
			'timestamp': 1624799291429,
			'source': {
				'type': 'user',
				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
			},
			'mode': 'active'
		}]
	}

	#line_body = received_message_1
	#line_body = received_message_2
	#event = new_follower_1
	#event = lost_follower_1

	replyToken, reply = line_bot(line_body)
	response = "Don't need to send a reply"
	if replyToken and reply:
		print('sending reply', reply, 'to', replyToken)
		response = api_to_line('reply', reply, replyToken)
	return HttpResponse(response)


def sendEmail(request):
	#send_mail('Test', 'This is a test', 'your@email.com', ['toemail@email.com'],
    #   fail_silently=False)
	return HttpResponse('This is the email response.')