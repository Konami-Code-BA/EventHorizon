<template>
	<div style="display: flex; flex-direction: column; align-items: center; padding-top: 5px;">
		<div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
			<input :placeholder="t('SEARCH')" :value="search" @input="setSearch" type="text" autocorrect="off"
					autocapitalize="none" style="width: 100% padding-bottom: 2px" v-on:keyup.enter="removeFocus()"
					id="search" autocomplete="off"/>
			<div style="width: 10px;"/>
			<button v-on:click.prevent="setSearch({target: {value: ''}})" class="no-border-button x-button">
				✖
			</button>
		</div>
		<div v-if="!noEvents" style="width: 100%; overflow-y: scroll; overflow-x: hidden; display: flex; flex-direction: column;
				align-items: center; padding-left: 10px; height: 100%;" id="scroller">
			<div style="width: 90%;">
				<div class="list">
					<div v-for="event in listEvents" class="event-card-item" style="">
						<button v-on:click.prevent="openEventModal(event.id)" class="no-border-button"
								style="width: 100%;" :id="`item${event.id}`">
							<event-block :event="event"/>
						</button>
					</div>
				</div>
			</div>
		</div>
		<div v-else style="font-size: 24px;">NO EVENTS</div>
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
				noEvents: false,
			}
		},
		watch: {
			'listEvents' () {
				if (this.listEvents.length === 0) {
					this.noEvents = true
				} else {
					this.noEvents = false
				}
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
			},
			removeFocus() {
				document.getElementById('search').blur()
			},
			setSearch (evt) {
				this.search = evt.target.value
				this.listEvents = f.filterEvents(
					this.store.events.display,
					this.search,
					['name', 'description', 'address', 'venue_name'])
			},
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
	.event-card-item {
		width:100%;
		height: 50px;
		margin: 6px auto;
	}
</style>
