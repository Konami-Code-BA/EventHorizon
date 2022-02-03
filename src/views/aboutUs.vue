<template>
	<div class="main">
		<br>
		ABOUT US
		<div style="width: 80%">
			<br>
	Event Horizon was started with the vision to bring people together, 
	to get involved with events that are fulfilling for hosts and attendees alike, 
	and to create a community of people who are always down for a good time. 
	With this in mind, we have been working on Event Horizon, a platform to assist 
	in the planning and execution of events, and a citywide bulletin board to make your event known. 
	Whether it's yoga in the park, international mixer, or anti-war protest, let Event Horizon help you!
	</div>
	</div>
	
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'aboutUs',
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
