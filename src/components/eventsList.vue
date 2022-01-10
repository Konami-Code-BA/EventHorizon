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
					<div v-for="event in listEvents">
						<button v-on:click.prevent="openEventModal(event.id)" class="no-border-button"
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
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'eventsList',
		data () {
			return {
				store: store,
				listEvents: null,
				selectedEvent: null,
				search: '',
				observer: new MutationObserver((mutations, obs) => {
					let el = document.getElementById(`item${this.selectedEvent.id}`)
					if (el) {
						this.scrollIt(el)
						return
					}
				}),
			}
		},
		watch: {
			'search' () {
				this.listEvents = f.filterEvents(
					this.store.events.display,
					this.search,
					['name', 'description', 'address', 'venue_name'])
			},
		},
		created () {
			this.listEvents = this.store.events.display
			if (!this.store.events.selected) {
				this.selectedEvent = f.getEventWithClosestFutureDate(this.listEvents, f.today)
			} else {
				this.selectedEvent = this.store.events.selected
			}
		},
		mounted () {
			this.observer.observe(document, {childList: true, subtree: true})
		},
		methods: {
			t (w) { return translations.t(w) },
			scrollIt () {
				let el = document.getElementById(`item${this.selectedEvent.id}`)
				let scroller = document.getElementById('scroller')
				let offsetTop = el.offsetTop
				scroller.scrollTop = el.offsetTop - scroller.offsetTop
			},
			openEventModal (id) {
				f.goToPage({ page: 'event', args: { id: id } })
			}
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