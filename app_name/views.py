from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
import json
import requests
	
def index(request):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def example(request):
	#req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
	#prepared = req.prepare()
	#req = request
	print('This is the webhook request _messages.', request._messages)
	print('This is the webhook request get_messages.', get_messages(request._messages))
	for message in get_messages(request._messages):
		print('This is a message:', message.message)
	print('This is the webhook request _stream.', request._stream.readline())
	#print('This is the webhook request 2.', list(request.POST))
	#print('This is the webhook request 1.', list(req.headers))
	#print('This is the webhook request 2.', list(req.POST))
	#print('This is the webhook request 3.', list(req.body))
	return HttpResponse('This is the webhook response.')
