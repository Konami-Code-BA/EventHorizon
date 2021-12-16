from rest_framework import serializers
from .models import User, Event
from collections import OrderedDict


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
	hosts = UserSerializer(read_only=True, many=True).data
	guests = UserSerializer(read_only=True, many=True).data
	confirmed_guests = UserSerializer(read_only=True, many=True).data
	interested_guests = UserSerializer(read_only=True, many=True).data
	invited_guests = UserSerializer(read_only=True, many=True).data

	class Meta:
		model = Event
		fields = '__all__'
	
	def __init__(self, data={}, context={}, *args, **kwargs):
		super(EventSerializer, self).__init__(self, data={}, context={}, *args, **kwargs)
		if 'user' in context:
			for event in data:
				if event != Event.objects.filter(guests=context['user'].id)[0]:
					if 'address' in self.fields:
						self.fields.pop('address')
						self.fields.pop('venue_name')
						self.fields.pop('hosts')
						self.fields.pop('guests')
						self.fields.pop('confirmed_guests')
						self.fields.pop('interested_guests')
						self.fields.pop('invited_guests')
						break

