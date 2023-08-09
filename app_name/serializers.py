from rest_framework import serializers
from .models import User, Event, Image, PlusOne


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['password']


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image


class PlusOneSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlusOne
