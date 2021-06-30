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
from app_name.functions import get_return_queryset
from app_name.functions import api_to_line


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
		response = eval(f"self.{request.data['command']}(request)")
		#queryset = None
		#serializer_data = None
		return Response(response)

	def consumption(self, request):
		response = api_to_line('consumption')
		print('consumption success:', response)
		return response

	def broadcast(self, request):
		response = api_to_line('broadcast', message=request.data['message'])
		print('broadcast success:', response)
		return response

	def push(self, request):
		mikeyOrStu = {
			'mikey': 'U09e3b108910c1711d2732a8b9ac8a19d',
			'stu': 'U7139ad1375429964a43e49031a509341',
		},
		response = api_to_line('push', message=request.data['message'], towho=mikeyOrStu[request.data['to']])
		print('push success:', response)
		return response

	def getAccessToken(self, request):
		params = {
			'grant_type': 'authorization_code',
			'code': request.data['code'],
			'redirect_uri': 'http://127.0.0.1:8080/experiment2',
			'client_id': '1656150937', # login channel
			'client_secret': 'db1b0a96dac4415e457efcaedb621ed1' # login channel
		}
		response = api_to_line('getAccessToken', params=params)
		print('we got the response', response, '\ntype', type(response))
		params = {
			'id_token': response['id_token'],
			'client_id': '1656150937', # login channel
		}
		response = api_to_line('verify', params=params)
		print('push success:', response)
		return response
