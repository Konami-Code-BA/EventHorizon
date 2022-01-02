<template>
	<div v-if="loaded">
		<div class="main" v-show="!showEventModal" style="padding-top: 5px;">
			<div style="display: flex; flex-direction: column; align-items: center;" v-if="!hideTop">
				<div style="font-size: 20px;" v-if="!isAuthenticatedUser">
					{{ t('REACH OUT TO NEW HORIZONS') }}
				</div>
				<div style="font-size: 20px;" v-else>
					{{ t('WELCOME') }}&nbsp;{{ store.user.display_name }}
				</div>
				<div>
					<img src="@/assets/eventhorizonLogo.png" style="max-width: 150px; max-height: 150px; z-index: 5">
				</div>
				<div style="font-size: 24px;">{{ t('EVENTS') }}:</div>
			</div>
			<div style="width: 100%;">
				<div style="position: fixed; margin-top: 15px; right: 2px; z-index: 10;">
					<button class="button" v-on:click.prevent="hideTop = !hideTop" style="border: 2px solid rgba(140, 128, 151, 0.6); border-radius: 7px; width: 25px; height: 25px; padding: 0; background-color: #18002e; padding-bottom: 1px;">
						<img src="@/assets/fullScreen.png" class="icon" style="width: 80%; height: 80%"/>
					</button>
				</div>
				<tabs :num-tabs="3" :initial="selectedTab" :key="selectedTab"
						@on-click="(arg) => { selectedTab = arg }"
						class="tabs">
					<div slot="1">
						<img src="@/assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="2">
						<img src="@/assets/calendarIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
					<div slot="3">
						<img src="@/assets/searchIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
				</tabs>
			</div>
			<events-map class="viewer" v-show="selectedTab==1" @openEventModal="openEventModal" :events="events"
					:selectedEventId="selectedEventId" :key="selectedEventId" :scrip="scrip" ref="eventsMap"
					:store="store"/>
			<events-calendar class="viewer" v-show="selectedTab==2" @openEventModal="openEventModal" :events="events"
					:store="store" :startingAt="selectedEventId"/>
			<events-list class="viewer" v-show="selectedTab==3" @openEventModal="openEventModal" :events="events"
					:store="store" :startingAt="selectedEventId" :key="selectedEventId+'list'"/>
		</div>
		<!--modal v-if="showCookiesModal" @closeModals="closeCookiesModal()">
			<div slot="contents" class="cookiesModal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="closeCookiesModal()" class="no-border-button x-button">
						✖
					</button>
				</div>
				<div style="white-space: pre-line; text-align: center; align-self: center; font-weight: 400;
						width: 80%;">
					{{t('THIS APP USES COOKIES')}}
				</div><br>
				<div style="align-self: center; width: 80%;">
					<button v-on:click.prevent="closeCookiesModal()" class="button" style="width: 100%">
						<big>{{t('OK')}}</big>
					</button>
				</div><br><br>
			</div>
		</modal-->
		<event v-if="showEventModal" @goToEvents="goToEvents()" :eventId="selectedEventId" @closeModals="closeEventModal()"/>
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
				store: store,
				showCookiesModal: store.user.alerts.includes(1),
				selectedTab: 1,
				showEventModal: Boolean(this.$route.params.id),
				selectedEventId: this.$route.params.id,
				events: null,
				loaded: false,
				scrip: document.createElement('script'),
				hideTop: false,
			}
		},
		computed : {
			isAuthenticatedUser () { return f.isAuthenticatedUser },
			today () { return new Date() },
		},
		watch: {
			'showEventModal' () {
				if (!this.showEventModal && this.$route.params.id) {
					this.$router.push({ name: 'events' })
				}
			},
			'loaded' () {
				this.$emit('endLoading')
			}
		},
		async created () {
			this.events = await api.getAllEvents()
			if (!this.selectedEventId) {
				this.selectedEventId = f.getEventWithClosestFutureDate(this.events, this.today)['id']
			}
			let apiKey = await api.secretsApi('google-maps-api-key')
			this.scrip.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
			this.scrip.async = true
			this.loaded = true
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
				this.selectedEventId = id
				this.showEventModal = true
			},
			closeEventModal () {
				// after closing, it goes to the previously opened event in map. should it also scroll to previously
				// opened event in the list and calendar?
				f.freeUpBackButton(this)
				this.$refs.eventsMap.initMap()
				this.showEventModal = false
			},
			goToEvents () {
				this.$refs.eventsMap.initMap()
				this.selectedTab = 1
				this.showEventModal = false
			},
			goToCalendar () {

			},
		} // methods
	} // export
</script>
<style scoped>
	.cookiesModal {
		position: fixed;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		z-index: 100;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}
	.tabs {
		background-color: rgba(0, 0, 0, .2);
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
		border-bottom: none !important;
	}
</style>
