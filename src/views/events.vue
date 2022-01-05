<template>
	<div v-if="loaded">
		<div class="main" v-show="!showEventModal" style="padding-top: 5px;">
			<div class="viewer filters" style="display: flex; flex-direction: column; align-items: center; height: 50%; width: 100%"
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
				<div style="border-bottom: 2px solid rgba(255, 255, 255, .3); width: 100%; display: flex;
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
				<div style="display: flex; flex-direction: column; align-items: flex-start; width: 100%; padding-top: 5px">
					<button class="people-button button" :class="{ selected : selectedFilter === 'all'}"
							v-on:click.prevent="selectedFilter = 'all'">
						{{ t('ALL') }}
					</button>
					<button class="people-button button"  :class="{ selected : selectedFilter === 'mine'}"
							v-on:click.prevent="selectedFilter = 'mine'">
						{{ t('MINE') }}
					</button>
					<button class="people-button button"  :class="{ selected : selectedFilter === 'allpeople'}"
							v-on:click.prevent="selectedFilter = 'allpeople'">
						{{ t('ALL PEOPLE I FOLLOW') }}
					</button>
					<button class="people-button button"  :class="{ selected : selectedFilter === 4}"
							v-on:click.prevent="selectedFilter = 4">
						
					</button>
					<button class="people-button button"  :class="{ selected : selectedFilter === 5}"
							v-on:click.prevent="selectedFilter = 5">
						
					</button>
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
					:events="displayEvents" :selectedEventId="selectedEventIdForMap" :scrip="scrip" ref="eventsMap"
					:store="store"
					:key="createKey(displayEvents, selectedEventIdForMap, 'map')"/>
			<events-list class="viewer events" v-show="selectedTab==2" @openEventModal="openEventModal"
					:events="displayEvents" :store="store" :startingAt="selectedEventIdForList"
					:key="createKey(displayEvents, selectedEventIdForList, 'list')"/>
			<events-calendar class="viewer events" v-show="selectedTab==3" @openEventModal="openEventModal"
					:events="displayEvents" :store="store"
					:key="createKey(displayEvents, 0, 'cal')"/>
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
		name: 'events',
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
				scrip: document.createElement('script'),
				hideTop: false,
				selectedFilter: 'all',
				showPeopleInfo: false,
			}
		},
		computed : {
			isAuthenticatedUser () { return f.isAuthenticatedUser },
			today () { return new Date() },
		},
		watch: {
			async 'selectedFilter' () {
				console.log(this.selectedFilter)
				this.displayEvents = this.events[this.selectedFilter]
				console.log(this.displayEvents)
				console.log(this.createKey(this.displayEvents, this.selectedEventIdForMap, 'map'))
				await this.$refs.eventsMap.initMap()
			},
		},
		async created () {
			this.events['all'] = await api.getAllEvents()
			this.displayEvents = this.events['all']
			this.events['mine'] = f.filterEvents(this.events, this.store.user.id, ['id'], false)
			let id = this.params.id
			if (id) {
				this.showEventModal = Boolean(this.params.id)
				this.openEventModal(id)
			} else {
				this.selectedEventIdForList = f.getEventWithClosestFutureDate(this.events, this.today)['id']
			}
			let apiKey = await api.secretsApi('google-maps-api-key')
			this.scrip.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
			this.scrip.async = true
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
				f.setBackButtonToCloseModal(this, window, this.closeEventModal)
				this.store.path = store.path + '/' + id
				this.selectedEventId = id
				this.selectedEventIdForList = id
				let event = f.filterEvents(this.events, id, ['id'], true)
				if (event.address) {
					this.selectedEventIdForMap = id
				}
				this.showEventModal = true
			},
			async closeEventModal () {
				f.freeUpBackButton(this)
				this.store.path = this.$route.path
				await this.$refs.eventsMap.initMap()
				this.showEventModal = false
			},
			goToMap () {
				this.closeEventModal()
				this.selectedTab = 1
			},
			createKey(displayEvents, eventId, letters) {
				let key = (displayEvents.length > 0 ? displayEvents[0]['id'] : 0).toString()
				key += (eventId ? eventId : 0).toString() + letters
				return key
			},
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
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		width: 100%;
	}
</style>
