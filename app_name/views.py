from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
import json
import requests
from app_name.functions import line_bot
from decouple import config

def index(request, arg=None):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def line_webhook(request):  # https://developers.line.biz/en/reference/messaging-api/#message-event
	line_body = json.loads(request.body.decode('utf-8'))
	send_to, reply = line_bot(line_body)
	response = "noReply"
	if send_to and reply:
		uri = 'reply' if send_to['type'] == 'replyToken' else 'push'
		url = 'https://api.line.me/v2/bot/message/' + uri
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = {
			send_to['type']: send_to['to'],
			'messages': [{
				'type': reply['type'],
			}]
		}
		if reply['type'] == 'text':
			data['messages'][0]['text'] = reply['text']
		elif reply['type'] == 'image':
			data['messages'][0]['originalContentUrl'] = reply['image']
			data['messages'][0]['previewImageUrl'] = reply['image']
		data = json.dumps(data)
		response = requests.post(url, headers=headers, data=data)
	return HttpResponse(response)
