import json
from decouple import config
from django.core.mail import send_mail
from django.conf import settings
import requests


# to run:
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
			if True:  # contact == 'mdsimeone@gmail.com':
				count += 1
				subject = 'Zak\'s Spring Fling Party!'
				message = f"""It's Zak! We got a Spring Fling at Aoyama Ever Club on April 8th (sat).
Omotesando. Party starts at 7:30pm and lasts until 10pm.
Entry costs guys ¥1,500 and girls ¥1,000 (show this email).
We have DJs and good vibes!
Re-entry okay. Hope to see you guys there!
BTW if you want Line messages: https://lin.ee/wPa66oQ
If you don't want emails anymore, just reply to this.

ザックです！土曜日4月8日にSpring Flingという春のパーティーあります！
表参道にある青山Ever Clubで、午後7時半〜10時。
入場料は男性1500円、女性1000円（このメールを見せてください）。
DJとかいます！再入場可能。会えるのを楽しみにしてるよ！
因みに、Lineメールを欲しかったら：https://lin.ee/wPa66oQ
Eメール欲しくないならこれ返事してくださいね"""
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [contact,]
				#send_mail(subject, message, email_from, recipient_list, fail_silently=False)
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
