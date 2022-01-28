<template>
	<div style="display: flex; flex-direction: column; align-items: center; padding-top: 5px;">
		<div>
			<input :placeholder="t('SEARCH')" v-model="search" type="text" autocorrect="off" autocapitalize="none"
					style="width: 100%"/>
		</div>
		<div style="width: 100%; overflow-y: scroll; overflow-x: hidden; display: flex; flex-direction: column;
				align-items: center; padding-left: 10px; height: 100%;" id="scroller">
			<div style="width: 90%;">
				<div class="list">
					<div v-for="event in listEvents" style="width: 100%; height: 50px;">
						<button v-on:click.prevent="openEventModal(event.id)" class="no-border-button"
								style="width: 100%;" :id="`item${event.id}`">
							<event-block :event="event"/>
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
	import eventBlock from '@/components/eventBlock.vue'
	export default {
		name: 'eventsList',
		components: {
			eventBlock,
		},
		data () {
			return {
				store: store,
				listEvents: null,
				selectedEvent: null,
				search: '',
				observer: null,
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
			if (this.selectedEvent) {
				this.observer = new MutationObserver((mutations, obs) => {
					let el = document.getElementById(`item${this.selectedEvent.id}`)
					if (el) {
						this.scrollIt(el)
						return
					}
				})
			}
		},
		mounted () {
			if (this.observer) {
				this.observer.observe(document, {childList: true, subtree: true})
			}
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
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: flex-start;
		overflow-x: hidden;
		overflow-y: visible;
		width: 100%;
		height: 100%;
		padding-top: 10px;
	}
</style>