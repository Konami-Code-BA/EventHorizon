<template>
	<div class="main">
		<br><br>
		<div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
			<br>
			<input :placeholder="t('SEARCH')" :value="search" @input="setSearch" type="text" autocorrect="off"
					autocapitalize="none" style="width: 100% padding-bottom: 2px" v-on:keyup.enter="removeFocus()"
					id="search" autocomplete="off"/>
			<div style="width: 10px;"/>
			<button v-on:click.prevent="search = ''" class="no-border-button x-button">
				✖
			</button>
		</div>
		
		<br>
		FAQ
		<div style="width:80%; overflow-y: scroll; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start;">
			<button class="no-border-button" v-on:click.prevent="display[1]=!display[1]"
					style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
					height: 50px; text-align: left; width: 100%">
				How can I host an event?&nbsp;
				<div v-if="display[1]">⇧</div>
				<div v-else>⇩</div>
			</button>
			<div v-show="display[1]">
				The hosting services are currently under construction and should be available in the coming 
				weeks/months. Until then, users can see upcoming events, including public events like festivals and 
				parties held by the app creators.
			</div>
			<button class="no-border-button" v-on:click.prevent="display[2]=!display[2]"
					style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
					height: 50px; text-align: left; width: 100%">
				What kind of events can we expect to see on this app?&nbsp;
				<div v-if="display[2]">⇧</div>
				<div v-else>⇩</div>
			</button>
			<div v-show="display[2]">
				This service was built with house/rental space parties in mind. After the release of the hosting 
				services, general users can plan and advertise any type of event (within reason, of course), such as 
				yoga sessions, flower viewing parties, international meet-ups, video game competitions; let your 
				imagination run wild!
			</div>
			<button class="no-border-button" v-on:click.prevent="display[3]=!display[3]"
					style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
					height: 50px; text-align: left; width: 100%">
				If I RSVP to an event, am I able to cancel last minute?&nbsp;
				<div v-if="display[3]">⇧</div>
				<div v-else>⇩</div>
			</button>
			<div v-show="display[3]">
				Event attendance is managed by the host of the event. If you need to cancel, please contact the host 
				through the EH portal or by other means. 
			</div>
			<button class="no-border-button" v-on:click.prevent="display[4]=!display[4]"
					style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
					height: 50px; text-align: left; width: 100%">
				Why can't I see an events specific location?&nbsp;
				<div v-if="display[4]">⇧</div>
				<div v-else>⇩</div>
			</button>
			<div v-show="display[4]">
				Some events are managed privately, and in order to prevent gatecrashing, some details of the event may 
				be kept hidden until the host verifies your identity. If you are interested in a private event, please 
				contact the host through the EH portal or by other means. 
			</div>
			<button class="no-border-button" v-on:click.prevent="display[5]=!display[5]"
					style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
					height: 50px; text-align: left; width: 100%">
				Do I need an account to attend events?&nbsp;
				<div v-if="display[5]">⇧</div>
				<div v-else>⇩</div>
			</button>
			<div v-show="display[5]">
				Attendance is managed by the host. If you know the host and can organise with them to attend the event 
				without using EH, then you can. EH is built to assist event planners by gathering all information 
				relating to the event in one place, so by making a free account and confirming through the app, it 
				would help the host out. Additionally, you'll be able to access information about other events and 
				parties happening in the city. 
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'faq',
		data () {
			return {
				search: '',
				display: {1: false, 2: false, 3: false, 4: false, 5: false,},
			}
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			setSearch (evt) {},

			removeFocus() {
				document.getElementById('search').blur()
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
