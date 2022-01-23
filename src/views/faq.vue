<template>
	<div class="main">
		FAQ
		<div style="width:80%; overflow-y: scroll">
How can I host an event? <br>
The hosting services are currently under construction and should be available in the coming weeks/months. Until then, users can see upcoming events, including public events like festivals and parties held by the app creators.
<br><br>
What kind of events can we expect to see on this app? <br>
This service was built with house/rental space parties in mind. After the release of the hosting services, general users can plan and advertise any type of event (within reason, of course), such as yoga sessions, flower viewing parties, international meet-ups, video game competitions; let your imagination run wild! 
<br><br>
If I RSVP to an event, am I able to cancel last minute? <br>
Event attendance is managed by the host of the event. If you need to cancel, please contact the host through the EH portal or by other means. 
<br><br>
Why can't I see an events specific location? <br>
Some events are managed privately, and in order to prevent gatecrashing, some details of the event may be kept hidden until the host verifies your identity. If you are interested in a private event, please contact the host through the EH portal or by other means. 
<br><br>
Do I need an account to attend events? <br>
Attendance is managed by the host. If you know the host and can organise with them to attend the event without using EH, then you can. 
EH is built to assist event planners by gathering all information relating to the event in one place, so by making a free account and confirming through the app, it would help the host out. Additionally, you'll be able to access information about other events and parties happening in the city. 
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'faq',
		data () {
			return {
			}
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
