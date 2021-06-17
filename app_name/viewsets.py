from rest_framework import viewsets, filters
from .models import User, Line
from .serializers import UserSerializer, LineSerializer
from rest_framework.response import Response
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from django.contrib import auth
from django.conf import settings
from django.contrib.sessions.models import Session


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ['=email', '=username',]

	#def list(self, request):  # GET {prefix}/
	def create(self, request):  # POST {prefix}/
		user = eval(f"self.{request.data['command']}(request)")
		print('user ', user, '\n', user.is_authenticated)
		if user.is_authenticated:
			print("HERE")
			queryset = [user]
			serializer = UserSerializer(queryset, many=True)
			return Response(serializer.data)
		else:
			return Response({'data': None})

	#def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
	#def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
	#def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
	#def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/

	
	def registration(self, request):
		username = request.data['username']
		email = request.data['email']
		password = request.data['password']
		user = User.objects.create_user(username=username, password=password, email=email)
		user.save()
		group = Group.objects.get(name='User')
		group.user_set.add(user)
		print('register')
		return user

	def login(self, request):
		username = request.data['username']
		password = request.data['password']
		user = auth.authenticate(username=username, password=password)
		if user is None:
			print('AUTHENTICATION FAILED')
			user = auth.models.AnonymousUser()
		else:
			auth.login(request, user)
		print('login')
		return user

	def logout(self, request):
		username = request.data['username']
		user = User.objects.get(username=username)
		auth.logout(request)
		print('logout')
		return user


	#def check(self, request):
	#	try:
	#		sessionid = request.session.session_key
	#		session = Session.objects.get(pk=sessionid)
	#		user_id = session.get_decoded()['_auth_user_id']
	#		user = User.objects.get(pk=user_id)
	#	except Session.DoesNotExist:
	#		print('exception')
	#		user = auth.models.AnonymousUser()
	#	return user



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
