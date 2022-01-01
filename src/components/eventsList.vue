<template>
	<div style="display: flex; flex-direction: column; align-items: center; padding-top: 5px;">
		<div>
			<input :placeholder="t('SEARCH')" v-model="search" type="text" id="email" autocorrect="off"
					autocapitalize="none" style="width: 100%"/>
		</div>
		<div style="width: 100%; overflow-y: scroll; overflow-x: hidden; display: flex; flex-direction: column;
				align-items: center">
			<div style="width: 90%;">
			<div class="list">
				<div v-for="event in sorted_events">
					<button v-on:click.prevent="$emit('openEventModal', event.id)" class="no-border-button"
							style="text-align: left; white-space: nowrap" :id="`item${event.id}`">
						{{ event.date_time.split('T')[0] }}: {{ event.name }}
					</button>
				</div>
			</div>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'eventsList',
		data () {
			return {
				sorted_events: {},
				search: null,
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
		watch: {
			'search' () {
				this.sorted_events = f.filterEvents(
					f.sortEventsByDate(this.events),
					this.search,
					['name', 'description', 'address', 'venue_name'])
			},
		},
		created () {
			this.sorted_events = f.sortEventsByDate(this.events)
		},
		mounted () {
			//if (this.startingAt) {
			//	console.log('HERE BRAH', this.startingAt)
			//	console.log(document.getElementById(this.startingAt).offsetTop)
			//	document.getElementById('view').scroll({left: 0, top: document.getElementById(`item${this.startingAt}`).offsetTop})
			//}
			//console.log(api.getEventWithClosestFutureDate(this.today))
			let id = f.getEventWithClosestFutureDate(this.events, this.today)['id']
			let el = document.getElementById(`item${id}`)
			let offsetTop = el.offsetTop
			console.log(offsetTop)
		},
		updated () {
		},
		methods: {
			t (w) { return translations.t(w) },
		}
	}
</script>
<style scoped>
	.list {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		overflow-x: hidden;
		overflow-y: visible;
	}
</style>