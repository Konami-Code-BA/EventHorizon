<template>
	<div class="list" id="view">
		<div style="align-self: center">
			{{ t('ALL EVENTS') }}:
		</div>
		<div v-for="event in sorted_events" :id="`item${event.id}`">
			<button v-on:click.prevent="$emit('openEventModal', event.id)" class="no-border-button"
					style="text-align: left; white-space: nowrap">
				{{ event.date_time.split('T')[0] }}: {{ event.id }}
			</button>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'eventsList',
		data () {
			return {
				sorted_events: {},
				loaded: false,
			}
		},
		components: {
		},
		props: {
			events: { default: null },
			store: { default: null },
			startingAt: { default: null },
		},
		computed: {
			today () {
				return new Date()
			},
		},
		created () {
			this.sorted_events = this.sortEventsByDate(this.events)
			//if (this.startingAt) {
			//	console.log('HERE BRAH', this.startingAt)
			//	console.log(document.getElementById(this.startingAt).offsetTop)
			//	document.getElementById('view').scroll({left: 0, top: document.getElementById(`item${this.startingAt}`).offsetTop})
			//}
			this.loaded = true
		},
		updated () {
		},
		methods: {
			t (w) { return translations.t(w) },
			sortEventsByDate (events) {
				return f.sortEventsByDate(events)
			},
		}
	}
</script>
<style scoped>
	.list {
		display: flex;
		flex-direction: column;
		overflow-y: scroll;
		overflow-x: hidden;
		align-items: flex-start;
	}
</style>