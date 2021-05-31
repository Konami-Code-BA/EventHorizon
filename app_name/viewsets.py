from rest_framework import viewsets, filters
from .models import User, Line
from .serializers import UserSerializer, LineSerializer
from rest_framework.response import Response
import requests
import json
from django.views.decorators.csrf import csrf_exempt


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ['=email', '=username',]


class LineViewset(viewsets.ViewSet):
	token = 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU='

	queryset = Line.objects.all()
	serializer = LineSerializer(queryset, many=True)
	def create(self, request):
		#print("REQUEST: " + request.data['command'])
		response = eval(f"self.{request.data['command']}(request)")
		#print("RESPONSE: ", response.json())

		saveit = Line(response=str(response))
		saveit.save()
		queryset = Line.objects.all()
		serializer = LineSerializer(queryset, many=True)
		return Response(serializer.data)

	def consumption(self, request):
		response = requests.get(
			'https://api.line.me/v2/bot/message/quota/consumption',
			headers = {
				'Authorization': 'Bearer ' + self.token,
			}
		)
		print("HERE", json.loads(response.content)['totalUsage'])
		response = json.loads(response.content)['totalUsage']
		return response

	def broadcast(self, request):
		message = request.data['message']
		response = requests.post(
			'https://api.line.me/v2/bot/message/broadcast',
			headers = {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + self.token,
			},
			data = json.dumps({
				#"to": "michaels234", 
				"messages": [
					{
						"type": "text",
						"text": message,
					}
				]
			})
		)
		response = 'Sent "' + message + '" to everyone'
		return response

	def push(self, request):
		message = request.data['message']
		response = requests.post(
			'https://api.line.me/v2/bot/message/push',
			headers = {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + self.token,
			},
			data = json.dumps({
				"to": 'U09e3b108910c1711d2732a8b9ac8a19d',
				"messages": [
					{
						"type": "text",
						"text": message,
					}
				]
			})
		)
		response = 'Sent "' + message + '" to Mikey'
		return response
