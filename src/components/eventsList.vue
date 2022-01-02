<template>
	<div style="display: flex; flex-direction: column; align-items: center; padding-top: 5px;">
		<div>
			<input :placeholder="t('SEARCH')" v-model="search" type="text" id="email" autocorrect="off"
					autocapitalize="none" style="width: 100%"/>
		</div>
		<div style="width: 100%; overflow-y: scroll; overflow-x: hidden; display: flex; flex-direction: column;
				align-items: center" id="scroller">
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
<script defer>
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'eventsList',
		data () {
			return {
				sorted_events: {},
				search: null,
				observer: new MutationObserver((mutations, obs) => {
					let el = document.getElementById(`item${this.startingAt}`)
					if (el) {
						this.scrollIt(el)
						return
					}
				}),
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
			this.observer.observe(document, {childList: true, subtree: true})
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			scrollIt () {
				let el = document.getElementById(`item${this.startingAt}`)
				let scroller = document.getElementById('scroller')
				let offsetTop = el.offsetTop
				scroller.scrollTop = el.offsetTop - scroller.offsetTop
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