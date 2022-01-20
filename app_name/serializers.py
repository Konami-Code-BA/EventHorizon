from rest_framework import serializers
from .models import User, Event, Image, PlusOne


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = '__all__'


class PlusOneSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlusOne
		fields = '__all__'
