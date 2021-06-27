from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
import json
import requests
from app_name.viewsets import UserViewSet, LineViewset
	
def index(request):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def example(request):
	line_body = json.loads(request.body.decode('utf-8'))
	#{
	#	'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
	#	'events': [
	#		{
	#			'type': 'message',
	#			'message': {
	#				'type': 'text',
	#				'id': '14296801432826',
	#				'text': 'Test message brah'
	#			},
	#			'timestamp': 1624799029188,
	#			'source': {
	#				'type': 'user',
	#				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
	#			},
	#			'replyToken': '3ef6d67db3304eebab8588ce2eff6331',
	#			'mode': 'active'
	#		}
	#	]
	#}
	#{
	#	'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
	#	'events': [
	#		{
	#			'type': 'unfollow',
	#			'timestamp': 1624799291429,
	#			'source': {
	#				'type': 'user',
	#				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
	#			},
	#			'mode': 'active'
	#		}
	#	]
	#}
	#{
	#	'destination': 'Ub480d7e5ff2b8357eb196ed6729bd689',
	#	'events': [
	#		{
	#			'type': 'follow',
	#			'timestamp': 1624799586678,
	#			'source': {
	#				'type': 'user',
	#				'userId': 'U09e3b108910c1711d2732a8b9ac8a19d'
	#			},
	#			'replyToken': 'be6008d01ab84e1a8ee7699102927f00',
	#			'mode': 'active'
	#		}
	#	]
	#}

	# either we have them make a username password or they login using line and get their line name, if possible.
	# "Integrating LINE Login with your web app"
	line_header = json.loads(request.headers.decode('utf-8'))

	return HttpResponse('This is the webhook response.')
