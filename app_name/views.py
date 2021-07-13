from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
import json
import requests
from app_name.functions import line_bot
from decouple import config

def index(request):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def line_webhook(request):
	line_body = json.loads(request.body.decode('utf-8'))
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
	line_body = new_follower_1
	#line_body = lost_follower_1

	replyToken, reply = line_bot(line_body)
	response = "Don't need to send a reply"
	if replyToken and reply:
		url = 'https://api.line.me/v2/bot/message/reply'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = json.dumps({
			'replyToken': replyToken,
			'messages': [{
				"type": "text",
				"text": reply,
			}]
		})
		response = requests.post(url, headers=headers, data=data)
	return HttpResponse(response)
