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
def line_webhook(request):  # https://developers.line.biz/en/reference/messaging-api/#message-event
	line_body = json.loads(request.body.decode('utf-8'))
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
