from rest_framework import viewsets, filters, permissions
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
from decouple import config
from django.core.mail import send_mail


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


class UserViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = serializer_class.Meta.model.objects.all()
	filter_backends = (filters.SearchFilter,)
	search_fields = ['=email', '=username',]

	def list(self, request):  # GET {prefix}/
		print('list', end=': ')
		return get_return_queryset(self, request)

	def retrieve(self, request, pk=None):  # GET {prefix}/{lookup}/
		print('retrieve', end=': ')
		return get_return_queryset(self, request, pk=pk)

	def update(self, request, pk=None):  # PUT {prefix}/{lookup}/
		print('request.data', request.data.user)
		print('update', end=': ')
		return get_return_queryset(self, request, pk=pk)

	def partial_update(self, request, pk=None):  # PATCH {prefix}/{lookup}/
		user = eval(f"self.{request.data['command']}(request, pk)")
		print('partial_update', end=': ')
		return get_return_queryset(self, request, pk=pk)
	
	def updateUserLanguage(self, request, pk):
		user = User.objects.get(pk=pk)
		user.language = request.data['language']
		user.save()
	
	def updateUserGetEmails(self, request, pk):
		user = User.objects.get(pk=pk)
		user.getEmails = request.data['getEmails']
		user.save()

	def destroy(self, request, pk=None):  # DELETE {prefix}/{lookup}/
		print('destroy', end=': ')
		return get_return_queryset(self, request, pk=pk)

	def create(self, request):  # POST {prefix}/
		print("DEBUG", config('PYTHON_ENV'), config('PYTHON_ENV', default='production') == 'development', settings.DEBUG)
		user = eval(f"self.{request.data['command']}(request)")
		print('create', end=': ')
		return get_return_queryset(self, request, pk=request.user.pk)

	def registration(self, request):
		username = request.data['username']
		email = request.data['email']
		password = request.data['password']
		language = request.data['language']
		user = User.objects.create_user(username=username, password=password, email=email, language=language)
		user.save()
		group = Group.objects.get(name='User')
		group.user_set.add(user)
		if user:
			auth.login(request, user)
		return user

	def login(self, request):
		username = request.data['username']
		password = request.data['password']
		user = auth.authenticate(username=username, password=password)
		if user:
			auth.login(request, user)
		print('login')
		return user

	def logout(self, request):
		username = request.data['username']
		user = User.objects.get(username=username)
		if user:
			auth.logout(request)
		print('logout')
		return user

	def authenticateFromSession(self, request):
		print('request.session', request.session.session_key)
		if request.session.session_key:
			session_key = request.session.session_key
			session = Session.objects.get(pk=session_key)
			user_id = session.get_decoded()['_auth_user_id']
			user = User.objects.get(pk=user_id)
			if user:
				auth.login(request, user)
		else:
			user = None
		return user
	
	def sendEmail(self, request):
		print('in the place')
		subject = 'Test sending email from site from mikey'
		message = 'Was I able to send it?'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['mdsimeone@gmail.com',]
		send_mail(subject, message, email_from, recipient_list, fail_silently=False)
		print('finished')


class LineViewset(viewsets.ViewSet):
	token = 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU='

	queryset = Line.objects.all()
	serializer_class = LineSerializer(queryset, many=True)
	def create(self, request):
		#print("REQUEST: " + request.data['command'])
		response = eval(f"self.{request.data['command']}(request)")
		#print("RESPONSE: ", response.json())

		saveit = Line(response=str(response))
		saveit.save()
		queryset = Line.objects.all()
		serializer = self.serializer_class(queryset, many=True)
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
