<template>
	<div v-if="loaded">
		<div class="main" v-show="!showEventModal" style="padding-top: 5px;">
			<div class="viewer filters" style="display: flex; flex-direction: column; align-items: center; height: 140px; width: 100%"
					v-if="!hideTop">
				<!--div style="font-size: 20px;" v-if="!isAuthenticatedUser">
					{{ t('REACH OUT TO NEW HORIZONS') }}
				</div>
				<div style="font-size: 20px;" v-else>
					{{ t('WELCOME') }}&nbsp;{{ store.user.display_name }}
				</div-->
				<!--div>
					<img src="@/assets/eventhorizonLogo.png" style="max-width: 150px; max-height: 150px; z-index: 5">
				</div>
				<div style="font-size: 24px;">{{ t('EVENTS') }}:</div-->
				<div style="border-bottom: 2px solid rgba(255, 255, 255, .3); width: 100%; display: flex; height: auto;
						justify-content: center">
					<div>
						{{ t('SELECT WHAT EVENTS TO DISPLAY') }}
					</div>
					<div style="position: absolute; right: 2%;">
						<button style="background: none; border: none"
								v-on:click.prevent="showPeopleInfo = !showPeopleInfo">
							<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="people-info"/>
						</button>
					</div>
				</div>
				<div style="display: flex; flex-direction: column; align-items: flex-start; width: 100%;
						padding-top: 5px; padding-bottom: 5px; height: auto;">
					<div style="display: flex; flex-direction: row; width: 100%;">
						<div>
							<input type="checkbox" class="checkbox" v-model="filters['all']" @click="filterChange('all')"/>
						</div>
						<button class="people-button button" :class="{ selected : filters['all']}"
								v-on:click.prevent="filters['all']=!filters['all']; filterChange('all')">
							<div>
								{{ t('ALL') }}
							</div>
						</button>
					</div>
					<div style="display: flex; flex-direction: row; width: 100%;">
						<div>
							<input type="checkbox" class="checkbox" v-model="filters['mine']" @click="filterChange('mine')"/>
						</div>
						<button class="people-button button" :class="{ selected : filters['mine']}"
								v-on:click.prevent="filters['mine']=!filters['mine']; filterChange('mine')">
							<div>
								{{ t('MINE') }}
							</div>
						</button>
					</div>
					<div style="display: flex; flex-direction: row; width: 100%;">
						<div>
							<input type="checkbox" class="checkbox" v-model="filters['allPeople']" @click="filterChange('allPeople')"/>
						</div>
						<button class="people-button button" :class="{ selected : filters['allPeople']}"
								v-on:click.prevent="filters['allPeople']=!filters['allPeople']; filterChange('allPeople')"
								disabled>
							<div>
								{{ t('PEOPLE I FOLLOW') }}
							</div>
							<div>
								<small>({{ t('COMING SOON') }})</small>
							</div>
						</button>
					</div>
				</div>
			</div>
			<div class="tabsdiv" style="width: 100%; display: flex; flex-direction: column;">
				<!--div style="position: fixed; margin-top: 15px; right: 2px; z-index: 10;">
					<button class="button" v-on:click.prevent="hideTop = !hideTop" style="border: 2px solid rgba(140, 128, 151, 0.6); border-radius: 7px; width: 25px; height: 25px; padding: 0; background-color: #18002e; padding-bottom: 1px;">
						<img src="@/assets/fullScreen.png" class="icon" style="width: 80%; height: 80%"/>
					</button>
				</div-->
				<div style="display: flex;
						justify-content: center">
					<div>
						{{ t('EVENTS') }}
					</div>
					<div style="position: absolute; right: 2%;">
						<button style="background: none; border: none"
								v-on:click.prevent="showEventsInfo = !showEventsInfo">
							<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="events-info"/>
						</button>
					</div>
				</div>
				<tabs :num-tabs="3" :initial="selectedTab" :key="selectedTab"
						@on-click="(arg) => { selectedTab = arg }"
						style="border-left: none; border-right: none; border-bottom: none;">
					<div slot="1">
						<img src="@/assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="2">
						<img src="@/assets/threeBarsHIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
					<div slot="3">
						<img src="@/assets/calendarIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
				</tabs>
			</div>
			<events-map class="viewer events" v-show="selectedTab==1" @openEventModal="openEventModal"
					:events="displayEvents" :selectedEventId="selectedEventIdForMap" ref="eventsMap"
					:store="store"
					:key="createComponentKey(selectedEventIdForMap, 'map')"/>
			<events-list class="viewer events" v-show="selectedTab==2" @openEventModal="openEventModal"
					:events="displayEvents" :store="store" :startingAt="selectedEventIdForList"
					:key="createComponentKey(selectedEventIdForList, 'list')"/>
			<events-calendar class="viewer events" v-show="selectedTab==3" @openEventModal="openEventModal"
					:events="displayEvents" :store="store"
					:key="createComponentKey(0, 'cal')"/>
		</div>
		<event v-if="showEventModal" @goToMap="goToMap()" :eventId="selectedEventId" @closeModals="closeEventModal()"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import tabs from '@/components/tabs.vue'
	import eventsMap from '@/components/eventsMap.vue'
	import eventsCalendar from '@/components/eventsCalendar.vue'
	import eventsList from '@/components/eventsList.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import event from '@/components/event.vue'
	export default {
		name: 'front',
		components: {
			modal,
			tabs,
			eventsMap,
			eventsCalendar,
			eventsList,
			event,
		},
		data () {
			return {
				params: this.$route.params,
				store: store,
				showCookiesModal: store.user.alerts.includes(1),
				selectedTab: 1,
				showEventModal: null,
				selectedEventId: null,
				selectedEventIdForMap: null,
				selectedEventIdForList: null,
				displayEvents: null,
				events: {},
				loaded: false,
				hideTop: false,
				filters: {'all': true, 'mine': false, 'allPeople': false},
				showPeopleInfo: false,
			}
		},
		computed : {
			isAuthenticatedUser () { return f.isAuthenticatedUser },
			today () { return new Date() },
		},
		watch: {
		},
		async created () {
			this.events['all'] = await api.getAllEvents()
			this.displayEvents = this.events['all']
			this.events['mine'] = f.filterEvents(this.displayEvents, this.store.user.id, ['invited'], false)
			this.events['none'] = []
			let id = this.params.id
			if (id) {
				this.showEventModal = Boolean(this.params.id)
				this.openEventModal(id)
			} else {
				this.selectedEventIdForList = f.getEventWithClosestFutureDate(this.displayEvents, this.today)['id']
			}

			let scrip = document.createElement('script')
			scrip.type = 'text/javascript'
			let apiKey = await api.secretsApi('google-maps-api-key')
			scrip.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
			document.head.appendChild(scrip)

			this.loaded = true
			this.$emit('endLoading')
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				await api.updateUserAlerts('Show Cookies')
			},
			openEventModal (id) {
				this.$emit('modalPage', 'event', id)
				this.selectedEventId = id
				this.selectedEventIdForList = id
				let event = f.filterEvents(this.events['all'], id, ['id'], true)
				if (event.address) {
					this.selectedEventIdForMap = id
				}
				this.showEventModal = true
			},
			async closeEventModal () {
				f.freeUpBackButton(this)
				this.store.path = this.$route.path
				window.initMap()
				this.showEventModal = false
			},
			goToMap () {
				this.closeEventModal()
				this.selectedTab = 1
			},
			createComponentKey(eventId, letters) {
				let key = (this.displayEvents.length > 0 ? this.displayEvents[0]['id'] : 0).toString()
				key += (eventId ? eventId : 0).toString() + letters
				return key
			},
			doFiltering () {
				this.displayEvents = []
				let keys = Object.keys(this.filters)
				for (let i = 0; i < keys.length; i++) {
					if (this.filters[keys[i]]) {  // if this filter is true
						this.displayEvents = this.displayEvents.concat(this.events[keys[i]])
					}
				}
				if (this.displayEvents.length > 0) {
					this.selectedEventIdForList = f.getEventWithClosestFutureDate(this.displayEvents, this.today)['id']
				}
				window.initMap(google)
			},
			filterChange (changed) {
				let keys = Object.keys(this.filters)
				if (changed === 'all') {  // if it was 'all' that changed
					if (this.filters[changed]) {  // if selected, deselect all others
						for (let i = 0; i < keys.length; i++) {
							if (keys[i] != changed) {
								this.filters[keys[i]] = false
							}
						}
					} else {  // if deselected, 'all' can only be deselected if its the only one selected, so
						this.filters['none'] = true  // make 'none' true
					}
				} else {  // if it was some other filter selection that changed
					if (this.filters[changed]) {  // if selected
						if (this.filters['all']) {  // deselect 'all' filter, if it is selected
							this.filters['all'] = false
						}
					} else {  // if deselected
						if (!Object.values(this.filters).includes(true)) {  // if no other filter is selected
							this.filters['none'] = true  // make 'none' true
						} // otherwise do nothing special, the changed filter has already been changed
					}
				}
				this.doFiltering()
			}
		} // methods
	} // export
</script>
<style scoped>
	.tabsdiv {
		background-color: rgba(0, 0, 0, .2);
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
		border: 2px solid rgba(255, 255, 255, .3);
	}
	.events {
		border-top: none;
		border-top-left-radius: 0;
		border-top-right-radius: 0;
	}
	.filters {
		
	}
	.selected {
		background-color: rgba(255, 255, 255, .2);  /*140,128,151,0.6 after combinging with #18002e*/
		width: 100%;
	}
	.people-button {
		border: none;
		border-radius: 0;
		height: 20px;
		padding: 10px;
		padding-left: 35px;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: flex-start;
		width: 100%;
	}
	/*.dual-set {
		display: flex;
		flex-direction: row;
		align-self: center;
		align-items: center;
		justify-content: center;
		padding: 0;
		width: 100%;
	}*/
	.checkbox {
		position: fixed;
		height: 15px;
		width: 20px;
	}
</style>
