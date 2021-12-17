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
					date_time: new Date('2021-12-31T03:24:00'),
					include_time: true,
					is_private: true,
					hosts: [],
					invited: [],
					confirmed_guests: [],
					interested: [],
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
