import requests, json, secrets
from decouple import config
from collections import namedtuple
from django.contrib.auth.models import Group
from django.contrib import auth
from .models import Alert, Event, PlusOne
from django.core.mail import send_mail
from django.conf import settings


def is_admin(request):  # is staff and is in the Admin group
	return request.user.is_staff and request.user.groups.filter(name='Admin').exists()


def is_admin_or_this_user(request, pk):  # is admin, or is a user that matches the pk
	return is_admin(request) or int(pk) == request.user.pk


# this doesnt work anymore, also im not sure how necessary it is. keeping it for now tho in case i want it later
#def get_return_queryset(self, request, pk=None):
#	if hasattr(request.user, 'error'):  # not a user, just an error
#		queryset = [request.user]
#	elif request.user.is_authenticated:  # is an authenticated user
#		if pk:  # trying to access one user
#			checker = is_admin_or_this_user(request, pk)  # check if is admin or is this user
#		else:  # trying to access all users
#			checker = is_admin(request)  # check if is admin
#		objects = self.serializer_class.Meta.model.objects
#		if checker:  # if accessing one user: is admin or is this user. if accessing all users, is admin
#			if pk:  # trying to access one user
#				try:
#					queryset = [objects.get(pk=pk)]  # get the user
#				except self.serializer_class.Meta.model.DoesNotExist:
#					user = namedtuple('user', 'error')
#					user.error = 'a user with this id could not be found'
#					queryset = [user]
#			else:  # trying to access all users
#				queryset = objects.all()  # get all users
#		else:  # is some user
#			if pk:  # trying to access one other user
#				user = namedtuple('user', 'error')
#				user.error = 'you don\'t have permission to access other users'
#				queryset = [user]
#			else:  # trying to access all users
#				queryset = [request.user]  # get only himself
#	else:  # unauthenticated user
#		user = namedtuple('user', 'error')
#		user.error = 'you are not an authenticated user'
#		queryset = [user]
#	if hasattr(queryset[0], 'error'):
#		serializer_data = [OrderedDict([('error', queryset[0].error)])]
#	else:
#		serializer_data = self.serializer_class(queryset, many=True).data
#	return Response(serializer_data)


def line_bot(line_body):
	replyToken, reply, received = None, None, None
	if len(line_body['events']) > 0:
		events = line_body['events'][0]
	else: 
		return replyToken, reply
	if events['type'] == 'follow':
		result = add_line_friend(events['source']['userId'])
		reply = {'type': 'text', 'text': result}
	if events['type'] == 'unfollow':
		remove_line_friend(events['source']['userId'])
	elif events['type'] == 'message':  # its a message (not a follow etc)
		if events['message']['type'] == 'text':  # its a text message (not an image etc)
			if events['message']['text'][0] == '.':  # it has a bot trigger
				received = events['message']['text'][1:]  # save the text minus the bot trigger
			elif events['source']['type'] == 'user':  # it doesn't have a bot trigger but it is a 1-user private room
				received = events['message']['text']  # private room doesn't need bot trigger, so save all the text
	if 'replyToken' in events:
		send_to = {'type': 'replyToken', 'to': events['replyToken']}
	if 'to' in events:
		send_to = {'type': 'to', 'to': events['to']}
	if received and ('status' in received or 'Status' in received):
		reply = {'type': 'text', 'text': 'Here is your status brah'}
	elif received and ('image' in received or 'Image' in received):
		reply = {'type': 'image', 'image': 'Here is your image brah'}  # need to send an image file not text here.
	return send_to, reply


def add_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		user.is_line_friend = True
		user.do_get_lines = True
		user.save()
		print('CHANGED is_line_friend AND do_get_lines FOR EXISTING LINE FRIEND')
		result = 'Thank you for following!'
	except UserViewset.model.DoesNotExist:  # if no user with this line id exists
		# this wasn't done on the site, it was done in line so there is no user, and can't make session
		#user = UserViewset.model.objects.create_user(  # create temporary line friend user
		#	line_id = line_id,
		#	do_get_lines = True,
		#	is_line_friend = True,
		#	display_name = 'Temp Line Friend', 
		#	do_get_line_display_name = True,
		#	random_secret = secrets.token_urlsafe(16)
		#)
		#user.groups.add(Group.objects.get(name='Temp Line Friend').id)  # temp line friend
		#user.save()
		#print('ADDED NEW TEMP LINE FRIEND')
		result = 'Thank you for following! Your Line account isn\'t connected to the site though. Please go to the site and register with Line in order to get Line messages / notifications about events. https://www.eventhorizon.vip'
	return result


def remove_line_friend(line_id):
	from app_name.viewsets import UserViewset
	try:  # if user with this line id exists
		user = UserViewset.model.objects.get(line_id=line_id)
		user.is_line_friend = False
		user.do_get_lines = False
		user.save()
	except UserViewset.model.DoesNotExist:  # this is basically not possible
		pass


def authenticate_login(request):
	user = auth.authenticate(request)
	if not hasattr(user, 'error'):
		auth.login(request, user)
	return user


def verify_update_line_info(user):  # user: existing user with line id & access token already gotten
	print('VERIFYING AND UPDATING LINE INFO')
	url = 'https://api.line.me/oauth2/v2.1/token'  # no matter if access token expired or not, refresh access token 1st
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	data = {
		'grant_type': 'refresh_token',
		'refresh_token': user.line_refresh_token,
		'client_id': config('LOGIN_CHANNEL_ID'),
		'client_secret': config('LOGIN_CHANNEL_SECRET'),
	}
	refreshAccessToken_response = json.loads(requests.post(url, headers=headers, data=data).content)
	# if refresh token is expired, this is session login attempt, block attempt and force them to click the line
	# login button and do a line login from the start
	if 'error' in refreshAccessToken_response:
		user = namedtuple('user', 'error')
		user.error = refreshAccessToken_response['error_description']
		return user
	# otherwise
	user.line_access_token = refreshAccessToken_response['access_token']  # save new refreshed access token to user data
	user.line_refresh_token = refreshAccessToken_response['refresh_token']  # also refresh token
	user.save()
	url = 'https://api.line.me/oauth2/v2.1/verify?access_token=' + user.line_access_token  # first verify access token
	verify_response = json.loads(requests.get(url).content)
	if verify_response['client_id'] != config('LOGIN_CHANNEL_ID'):  # make sure verification not intercepted
		user = namedtuple('user', 'error')
		user.error = 'could not verify client id when trying to verify access token'
		return user  # client id can't be confirmed
	#request.data['line_id'] = user.line_id
	#user = authenticate_login(request)  # login again just in case, and to get new location info
	return user


def new_visitor(request):
	from app_name.viewsets import UserViewset, SecretsViewset
	for i in range(1000):
		random_secret = secrets.token_urlsafe(16)
		try:
			user = UserViewset.model.objects.get(random_secret=random_secret)
		except UserViewset.model.MultipleObjectsReturned:
			pass
		except UserViewset.model.DoesNotExist:
			break
	user = UserViewset.model.objects.create_user(
		random_secret = random_secret,
		display_name = 'Temp Visitor',
	)
	user.save()
	group = Group.objects.get(id=3)
	group.user_set.add(user)
	alert = Alert.objects.get(name='Show Cookies')
	alert.user_set.add(user)
	request.data['random_secret'] = user.random_secret
	auth.login(request, user)
	return user


def merge_users(current_user, merge_user):
	print('MERGING USERS')
	# merge user field info
	if current_user.display_name == 'Temp Line Friend':
		current_user.display_name = merge_user.display_name
	if merge_user.line_id:
		current_user.line_id = merge_user.line_id
		current_user.line_access_token = merge_user.line_access_token
		current_user.line_refresh_token = merge_user.line_refresh_token
	current_user.do_get_line_display_name = current_user.do_get_line_display_name and merge_user.do_get_line_display_name
	current_user.is_line_friend = current_user.is_line_friend or merge_user.is_line_friend
	current_user.do_get_lines = current_user.do_get_lines or merge_user.do_get_lines
	if merge_user.email:
		current_user.email = merge_user.email
		current_user.password = merge_user.password
	current_user.do_get_emails = current_user.do_get_emails or merge_user.do_get_emails
	if merge_user.date_joined < current_user.date_joined:
		current_user.date_joined = merge_user.date_joined
	current_user.visit_count += merge_user.visit_count
	current_user.is_staff = current_user.is_staff or merge_user.is_staff
	current_user.is_superuser = current_user.is_superuser or merge_user.is_superuser
	current_user.save()
	# merge events
	events = Event.objects.filter(invited=merge_user.id)
	for event in events:
		event.invited.remove(merge_user.id)
		event.invited.add(current_user.id)
		if event.hosts.filter(id=merge_user.id).exists():
			event.hosts.remove(merge_user.id)
			event.hosts.add(current_user.id)
		if event.maybe.filter(id=merge_user.id).exists():
			event.maybe.remove(merge_user.id)
			event.maybe.add(current_user.id)
		if event.attending.filter(id=merge_user.id).exists():
			event.attending.remove(merge_user.id)
			event.attending.add(current_user.id)
		if event.wait_list.filter(id=merge_user.id).exists():
			event.wait_list.remove(merge_user.id)
			event.wait_list.add(current_user.id)
		if event.invite_request.filter(id=merge_user.id).exists():
			event.invite_request.remove(merge_user.id)
			event.invite_request.add(current_user.id)
	# merge plus_ones
	plus_ones = PlusOne.objects.filter(chaperone=merge_user.id)
	for plus_one in plus_ones:
		plus_one.chaperone.remove(merge_user.id)
		plus_one.chaperone.add(current_user.id)
	merge_user.delete()
	return current_user


def user_in_guest_statuses(event, user_id, guest_statuses):
	for guest_status in guest_statuses:
		if getattr(event, guest_status).filter(id=user_id).exists():
			return True
	return False


def notify_user(user, message, notification_type='other'):
	# only send line if user.do_get_lines (of course)
	# or its a DM and, you have a line and don't have an email at all
	if user.do_get_lines or (notification_type == 'DM' and user.line_id and (not user.email)):
		data = {"to": user.line_id, "messages": [{"type": "text", "text": message}]}
		url = 'https://api.line.me/v2/bot/message/push'
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		}
		data = json.dumps(data)
		requests.post(url, headers=headers, data=data)
	# only send email if user.do_get_emails (of course)
	# or its a DM and, you have an amil and (don't want / can't receive lines)
	# Note: this way...
	# if has line and doesn't have email, it'll send line
	# if has email and doesn't have line, it'll send email
	# if has line and email but both marked off, it'll not send line, it will send email
	if user.do_get_emails or (notification_type == 'DM' and user.email and (not user.do_get_lines)):
		subject = 'Event Horizon Notification'
		message = message
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [user.email,]
		send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def feedback(message):
	subject = 'FEEDBACK'
	message = message
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [settings.EMAIL_HOST_USER,]
	send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def impossibly_over_attending_limit(event, changing_user_id, change_is_plus_one=False):
	# affecting attending if change is plus one and changing user is attending
	# note: assume if not change_is_plus_one, we are adding changing_user to attending. otherwise we wouldn't be
	# calling this function
	if (
		change_is_plus_one and event.attending.filter(id=changing_user_id).exists()
	):
		attending_count = event.attending.count()
		filled_space = 1  # changing_user or plus_one is entering attending, so automatically 1 filled space
		for plus_one in event.plus_ones.all():  # add attending plus_ones to attending count
			chaperone_id = plus_one.chaperone.all().values_list('id', flat=True)[0]
			if event.attending.filter(id=chaperone_id).exists():  # if plus_one's chaperone is attending
				attending_count += 1
			# note: if change_is_plus_one, we haven't added the plus one yet. and since user can only have 1 plus_one,
			# it's impossible for this to add 2nd plus_one in the case of change_is_plus_one
			if chaperone_id == changing_user_id:  # if changing_user has plus_one, he's joining too
				filled_space += 1
		space = event.attending_limit - (attending_count + filled_space)  # eg. 20 - (19 + 2) = 20 - 21 = -1
		return space < 0  # space 0 is ok, but space -1 is impossible
	else:  # no affect on attending
		return False  # so won't go impossibly_over_attending_limit


def notify_waiting_users_if_necessary(event, changing_user_id, selected_status=None, change_is_plus_one=0):
	# note: this doesn't prevent going over attending limit, that is checked elsewhere
	# note: this is run before changes are made to attending counts, so that we know whether we've gone over/under limit
	# if changing_user is in attending and, his plus_one is leaving or he is
	if (event.attending.filter(id=changing_user_id).exists()
			and (change_is_plus_one == -1 or (change_is_plus_one == 0 and selected_status != 'attending'))):
		attending_count = event.attending.count()
		opened_space = 1  # changing_user or his plus_one is leaving attending, so automatically 1 opened space
		for plus_one in event.plus_ones.all():  # add attending plus_ones to attending count
			chaperone_id = plus_one.chaperone.all().values_list('id', flat=True)[0]
			if event.attending.filter(id=chaperone_id).exists():  # if plus_one's chaperone is attending
				attending_count += 1
			if chaperone_id == changing_user_id:  # if changing_user has plus_one, he's leaving with him
				opened_space += 1 + change_is_plus_one  # but if its his plus_one that's leaving, we already counted him
		space = event.attending_limit - (attending_count - opened_space)  # eg. 20 - (21 - 2) = 20 - 19 = 1
		# if space is 1 or more, it's possible a waiting_user could enter; notify them if so.
		if (space >= 1):
			for waiting_user in event.wait_list.all():
				# notify if attending_count was impossible to enter with a plus_one and now there are 2 spaces or more.
				# or if attending_count was impossible to enter without a plus_one but now there is 1 space.
				# and don't notify the user who is entering attending
				if (
						((
							attending_count >= event.attending_limit - 1
							and event.plus_ones.filter(chaperone=waiting_user.id).exists()
							and space >= 2
						) or (
							attending_count >= event.attending_limit
							and (not event.plus_ones.filter(chaperone=waiting_user.id).exists())
							and space >= 1
						)) and waiting_user.id != changing_user_id
				):
					notify_user(
						waiting_user,
						f"""Event: {event.name}

Notification:
Space has opened up to attend the event!


To view this event, go here: {create_url(f'/?page=event&id={event.id}')}

To turn off notifications, go here: {create_url('/?page=settings')}
To message the host: go to the event (above link) ⇨ Show People ⇨ Hosts
*Note: you can't reply to this message here""",
					)
	# if changing_user is not in attending and he is entering, or he is in attending and he's adding a plus_one
	elif (((not event.attending.filter(id=changing_user_id).exists()) and selected_status == 'attending')
			or (event.attending.filter(id=changing_user_id).exists() and change_is_plus_one == 1)):
		attending_count = event.attending.count()
		filled_space = 1  # changing_user or his plus_one is entering attending, so automatically 1 filled space
		for plus_one in event.plus_ones.all():  # add attending plus_ones to attending count
			chaperone_id = plus_one.chaperone.all().values_list('id', flat=True)[0]
			if event.attending.filter(id=chaperone_id).exists():  # if plus_one's chaperone is attending
				attending_count += 1
			if chaperone_id == changing_user_id:  # if changing_user has plus_one, he's joining with him
				filled_space += 1  # but if change_is_plus_one, no problem, +1 doesnt exist yet so this won't happen
		space = event.attending_limit - (attending_count + filled_space)  # eg. 20 - (19 + 2) = 20 - 21 = -1
		# if space is 1 or less, it's possible a waiting_user with a plus_one can't enter anymore; notify them if so.
		if (space <= 1):
			for waiting_user in event.wait_list.all():
				# notify if attending_count was possible to enter with a plus_one and now there's only 1 space or less.
				# or if attending_count was possible to enter without a plus_one but now there are 0 spaces.
				# and don't notify the user who is entering attending
				if (
						((
							attending_count <= event.attending_limit - 2
							and event.plus_ones.filter(chaperone=waiting_user.id).exists()
							and space <= 1
						) or (
							attending_count <= event.attending_limit - 1
							and (not event.plus_ones.filter(chaperone=waiting_user.id).exists())
							and space <= 0
						)) and waiting_user.id != changing_user_id
				):
					notify_user(
						waiting_user,
						f"""Event: {event.name}

Notification:
There is no more space to attend the event :(


To view this event, go here: {create_url(f'/?page=event&id={event.id}')}

To turn off notifications, go here: {create_url('/?page=settings')}
To message the host: go to the event (above link) ⇨ Show People ⇨ Hosts
*Note: you can't reply to this message here""",
					)
	# if changing_user isn't altering attending
	else:
		attending_count = event.attending.count()
		for plus_one in event.plus_ones.all():  # add attending plus_ones to attending count
			chaperone_id = plus_one.chaperone.all().values_list('id', flat=True)[0]
			if event.attending.filter(id=chaperone_id).exists():  # if plus_one's chaperone is attending
				attending_count += 1
		space = event.attending_limit - attending_count
	return space <= 0  # space of 0 or less means it is_over_attending_limit after this change.


def create_url(path):
	if config('PYTHON_ENV', default='\'"production"\'') == 'development':
		url = 'http://127.0.0.1:8080' + path
	elif config('PYTHON_ENV', default='\'"production"\'') == '\'"test"\'':
		url = 'https://event-horizon-test.herokuapp.com' + path
	else:
		url = 'https://www.eventhorizon.vip' + path
	return url
