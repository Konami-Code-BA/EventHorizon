import json
#from decouple import config
#from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import base64
#import requests


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
			# ALWAYS TEST WITH YOURSELF FIRST ##########################################################################
			if contact == 'mdsimeone@gmail.com':  # True:  # 
				count += 1
				subject = 'Swimsuit Bikini Party! Aug 12'
				text_content = f"""Hey guys, zak is having an event, a swimsuit/bikini party at Aoyama ever club in Omotesando with ¥300 shots, so come stop by with your friends. 

Location: 青山ever (in Omotesando)
Time: Saturday august 12, 9pm to 2am
Price: guys ¥2,000 girls ¥1,500 (¥1,000 if bikini worn, at least the top) 
Re-entry okay 

皆さん、zak は Event Horizon でイベントをやります！今回は表参道の青山エバークラブでの水着・ビキニパーティーです。 300円ショットもありますので、お友達とぜひ来てください！

場所：青山エバー（表参道内）
時間: 8月12日土曜日、午後9時から午前2時まで
料金：男子 2,000円 女子 1,500円（ビキニトップ着用場合は1,000円）
再入場OK"""
				html_content = f"""
<p><img src="https://i.imgur.com/MbmBmZ6.jpg"></p>
<p>Hey guys, zak is having an event, a swimsuit/bikini party at Aoyama ever club in Omotesando with ¥300 shots, so come stop by with your friends. </p>
<br>
<p>Location: 青山ever (in Omotesando)</p>
<p>Time: Saturday august 12, 9pm to 2am</p>
<p>Price: guys ¥2,000 girls ¥1,500 (¥1,000 if bikini worn, at least the top) </p>
<p>Re-entry okay </p>
<br>
<p>皆さん、zak は Event Horizon でイベントをやります！</p>
<p>今回は表参道の青山エバークラブでの水着・ビキニパーティーです。 </p>
<p>300円ショットもありますので、お友達とぜひ来てください！</p>
<br>
<p>場所：青山エバー（表参道内）</p>
<p>時間: 8月12日土曜日、午後9時から午前2時まで</p>
<p>料金：男子 2,000円 女子 1,500円（ビキニトップ着用場合は1,000円）</p>
<p>再入場OK</p>
"""
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [contact,]
				#send_mail(subject, message, email_from, recipient_list, fail_silently=False)
				msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				print(f"{i+1}, id: {item[0]}, lang: {item[11]}, email: {contact}, name: {name}")
		# THIS IS FOR LINE, BUT WE CAN USE THE APP FOR NOW
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
