from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from app_name.functions import new_user_from_request


class UserBackend(BaseAuthentication):
	UserModel = get_user_model()
	def authenticate(self, request):
		if ('email' in request.data and 'password' in request.data and request.data['email'] != '' and
				request.data['password'] != ''):
			try:
				user = self.UserModel.objects.get(email=request.data['email'])
			except self.UserModel.DoesNotExist:
				return None
			if user.check_password(request.data['password']):
				return user
			else:
				return None
		elif 'line_id' in request.data and request.data['line_id'] != '':
			try:
				user = self.UserModel.objects.get(line_id=request.data['line_id'])
				return user
			except self.UserModel.DoesNotExist:
				return None
		elif request.session.session_key:
			session = Session.objects.get(pk=request.session.session_key)
			user_id = session.get_decoded()['_auth_user_id']
			try:
				user = self.UserModel.objects.get(pk=user_id)
				return user
			except self.UserModel.DoesNotExist:
				return None
		else:
			user = new_user_from_request(request)
			return None

	def get_user(self, user_id):
		try:
			return self.UserModel.objects.get(pk=user_id)
		except self.UserModel.DoesNotExist:
			return None