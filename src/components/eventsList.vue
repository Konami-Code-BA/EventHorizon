<template>
	<div style="display: flex; flex-direction: column; overflow-y: scroll; overflow-x: hidden; align-items: flex-start">
		<div style="align-self: center">
			{{ t('ALL EVENTS') }}:
		</div>
		<div v-for="event in sorted_events">
			<button v-on:click.prevent="$emit('openEventModal', event['id'])" class="no-border-button"
					style="text-align: left; white-space: nowrap">
				{{event['date_time'].split('T')[0]}}: {{event['name']}}
			</button>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
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
		},
		computed: {
			today () {
				return new Date()
			},
		},
		created () {
			this.selectedMonth = this.today.getMonth()  // note: month goes from 0 to 11 (so dumb)
			this.selectedYear = this.today.getYear() - 100 + 2000
			this.sortEventsByDate()
			this.loaded = true
		},
		methods: {
			t (w) { return translations.t(w) },
			sortEventsByDate () {
				this.sorted_events = this.events.sort((a, b) => {
					if (Date(a['date_time']) > Date(b['date_time'])) {
						return 1
					} else if (Date(a['date_time']) < Date(b['date_time'])) {
						return -1
					} else {
						return 0
					}
				})
			},
		}
	}
</script>
<style scoped>
</style>