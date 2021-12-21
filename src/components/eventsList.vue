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
				<div v-for="event in sorted_events" :id="`item${event.id}`">
					<button v-on:click.prevent="$emit('openEventModal', event.id)" class="no-border-button"
							style="text-align: left; white-space: nowrap">
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
	export default {
		name: 'eventsList',
		data () {
			return {
				sorted_events: {},
				loaded: false,
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
					this.sortEventsByDate(this.events),
					this.search,
					['name', 'description', 'address', 'venue_name'])
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
		align-items: flex-start;
		overflow-x: hidden;
		overflow-y: visible;
	}
</style>