from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from collections import namedtuple
from django.contrib.auth import login as auth_login


class UserBackend(BaseAuthentication):
	UserModel = get_user_model()
	def authenticate(self, request):
		print('***AUTHENTICATION START***')
		print(request.data)
		#return self.UserModel.objects.filter(email='mdsimeone@gmail.com').first()  # FOR EMERGENCY LOGIN
		if 'email' in request.data:
			try:
				print('email')
				user = self.UserModel.objects.get(email=request.data['email'])
				if user.check_password(request.data['code']):
					return user
				else:
					print('code fail')
					user = namedtuple('user', 'error')
					user.error = 'Incorrect code'
					return user
			except self.UserModel.DoesNotExist:
				print('DoesNotExist fail')
				user = namedtuple('user', 'error')
				user.error = 'This email is not registered'
				return user
			except BaseException as error:
				print('BaseException fail')
				user = namedtuple('user', 'error')
				user.error = error
				return user
		elif request.session.session_key:
			try:
				print('session')
				session = Session.objects.get(pk=request.session.session_key)
				user_id = session.get_decoded()['_auth_user_id']
				user = self.UserModel.objects.get(pk=int(user_id))
				#if user.line_id != '':  # if user has a line id, verify and refresh it
				#	result = verify_update_line_info(user)  # if refresh fails it won't login by session
				#	if hasattr(result, 'error'):
				#		user = namedtuple('user', 'error')
				#		user.error = 'line couldn\'t be verified'
				#		return user
				return user
			except self.UserModel.DoesNotExist:
				print('DoesNotExist fail')
				user = namedtuple('user', 'error')
				user.error = 'DoesNotExist'
				return user
		# missing email / password / line id / random secret / session info
		print('no possible login')
		user = namedtuple('user', 'error')
		user.error = 'none'
		return user

	def get_user(self, user_id):
		try:
			return self.UserModel.objects.get(pk=user_id)
		except self.UserModel.DoesNotExist:
			user = namedtuple('user', 'error')
			user.error = 'a user with this id could not be found'
			return user

	def login(self, request, user):
		auth_login(request, user)
