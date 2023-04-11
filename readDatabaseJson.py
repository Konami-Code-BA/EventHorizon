import json
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
import requests


# to run:
# change commented stuff as explained below, and save
# venv\Scripts\activate venv
# python manage.py shell
# import readDatabaseJson; readDatabaseJson.main()
def main():
	file1 = open('eventhorizonDatabaseJsonImportant.json', encoding="utf8")
	result = json.load(file1)
	print('line + email:', len(result['values']))
	count = 0
	for i in range(len(result['values'])):
		item = result['values'][i]
		name = item[16]
		if item[7]:  # EMAIL
			contact = item[7]
			# ALWAYS TEST WITH YOURSELF FIRST ONCE
			if contact == 'mdsimeone@gmail.com':  # True:  # 
				count += 1
				subject = 'Art and Music Event 1000¥!'
				message = f"""An Art and Music event will be held at Toggle Hotel Suidobashi, an Instagrammable luxury hotel located a 5-minute walk from the west exit of JR Suidobashi Station in the city center

TIME: 4/29 (SAT) 17:00-23:00
Live performance: 
1st set 18:30 
2nd set 21:00
PLACE: 9F Toggle Hotel Suidobashi (5min walk from JR Suidobashi station)
Entrance: 1000¥
BTW if you want Line messages: https://lin.ee/wPa66oQ
If you don't want emails anymore, just reply to this.

都心のJR水道橋駅の西口から徒歩5分にあるインスタ映えするラグジュアリーホテルToggle Hotel SuidobashiにてArtとMusicのイベントをやります。
テラスもあるのでいい景色を見ながらお酒をゆっくり飲むのもありですね。
1000円という破格な入場料なので友達と遊びに来てください！
ちなみに、LINEでの連絡を希望する場合はこちら：https://lin.ee/wPa66oQ
Eメールを希望しない場合は、このメールに返信してください"""
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [contact,]
				# UNCOMMENT THIS IN ORDER TO SEND
				# send_mail(subject, message, email_from, recipient_list, fail_silently=False)
				print(f"{i+1}, id: {item[0]}, lang: {item[11]}, email: {contact}, name: {name}")
		#if item[13]:  # LINE
		#	contact = item[13]
		#	to_print += f", line: {contact}, name: {name}rea"
		#	if 'Mikey' in name:
		#		message = ''
		#		data = {"to": contact, "messages": [{"type": "text", "text": message}]}
		#		url = 'https://api.line.me/v2/bot/message/push'
		#		headers = {
		#			'Content-Type': 'application/json',
		#			'Authorization': 'Bearer ' + config('MESSAGING_CHANNEL_ACCESS_TOKEN'),
		#		}
		#		data = json.dumps(data)
		#		requests.post(url, headers=headers, data=data)
	print('total sent:', count)
