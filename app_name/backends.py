from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from app_name.functions import verify_update_line_info


class UserBackend(BaseAuthentication):
	UserModel = get_user_model()
	def authenticate(self, request):
		#return self.UserModel.objects.get(email='mdsimeone@gmail.com')  # FOR EMERGENCY LOGIN
		if ('email' in request.data and 'password' in request.data and request.data['email'] != '' and
				request.data['password'] != ''):  # when logging in or registering by email
			try:
				user = self.UserModel.objects.get(email=request.data['email'])
				if user.check_password(request.data['password']):
					return user
				else:
					return None
			except self.UserModel.DoesNotExist:
				return None
		elif 'line_id' in request.data and request.data['line_id'] != '':  # when new line device
			try:
				user = self.UserModel.objects.get(line_id=request.data['line_id'])

				return user
			except self.UserModel.DoesNotExist:
				return None
		elif 'random_secret' in request.data and request.data['random_secret'] != '':  # when loggin in by random_secret
			try:
				user = self.UserModel.objects.get(random_secret=request.data['random_secret'])
				return user
			except self.UserModel.DoesNotExist:
				return None
		elif request.session.session_key:  # when loggin in from session
			session = Session.objects.get(pk=request.session.session_key)
			user_id = session.get_decoded()['_auth_user_id']
			try:
				user = self.UserModel.objects.get(pk=int(user_id))
				if user.line_id != '':  # if user has a line id, verify and refresh it
					user = verify_update_line_info(request, user)  # if refresh fails it won't login by session
				return user
			except self.UserModel.DoesNotExist:
				return None
		else:
			return None

	def get_user(self, user_id):
		try:
			return self.UserModel.objects.get(pk=user_id)
		except self.UserModel.DoesNotExist:
			return None