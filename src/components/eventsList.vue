<template>
	<div style="display: flex; flex-direction: column; overflow: scroll">
		<div style="align-self: center">
			{{ t('ALL EVENTS') }}:
		</div>
		<div v-for="event in eventDates">
			<button v-on:click.prevent="$emit('openEventModal', event[0]['id'])" class="no-border-button">
				{{event[0]['date_time'].split('T')[0]}}: {{event[0]['name'].split('T')[0]}}
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
				eventDates: {},
				loaded: false,
			}
		},
		components: {
		},
		props: {
			events: { default: null },
		},
		computed: {
			today () {
				return new Date()
			},
		},
		created () {
			this.selectedMonth = this.today.getMonth()  // note: month goes from 0 to 11 (so dumb)
			this.selectedYear = this.today.getYear() - 100 + 2000
			this.getAllEvents()
			this.loaded = true
		},
		methods: {
			t (w) { return translations.t(w) },
			getAllEvents () {
				for ( let i = 0; i < this.events.length; i++) {
					let dateTime = new Date(this.events[i]['date_time'])
					let date = new Date(
						dateTime.getYear() - 100 + 2000, dateTime.getMonth(), dateTime.getDate(), 0, 0, 0, 0
					).getTime()
					if (date in this.eventDates) {
						this.eventDates[date].push(this.events[i])
					} else {
						this.eventDates[date] = [this.events[i]]
					}
				}
			},
		}
	}
</script>
<style scoped>
</style>