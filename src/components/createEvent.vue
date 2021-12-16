<template>
	<div class="main">
		<div style="font-size: 36px;">NEW EVENT</div>
		<div class="line-height"></div>
		<div style="font-size: 24px;">{{ store.user.display_name }}</div>
		<div class="line-height"></div>
		<div class="coming-soon-list">
			<button v-on:click.prevent="createEvent()">CREATE EVENT</button>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registerWithEmailInternal',
		components: {
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
		},
		async mounted () {
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			async createEvent () {
				await apiFunctions.createEvent({  // lets make this a form
					name: 'name',
					description: 'description',
					address: '〒160-0023 東京都新宿区西新宿３丁目２−9',
					venue_name: 'venue_name',
					date_time: new Date(),
					include_time: true,
					is_private: false,
					hosts: [387],
					guests: [387],
					confirmed_guests: [387],
					interested_guests: [387],
					invited_guests: [387],
				})
			}
		} // methods
	} // export
</script>
<style scoped>
	.coming-soon-list {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		color: grey;
	}
</style>
