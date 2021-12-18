<template>
	<div v-if="loaded">
		<div class="main" v-show="!showEventModal">
			<div>
				<img src="@/assets/eventhorizonLogo.png" style="max-width: 150px; max-height: 150px; z-index: 5">
			</div>
			<!--div style="font-size: 38px; margin-bottom: 5px; position: fixed; top: 90px">EVENT HORIZON</div-->
			<div style="width: 100%;">
				<tabs :num-tabs="4" :not-buttons="[1]" :initial="selectedTab" :key="selectedTab"
						@on-click="(arg) => { selectedTab = arg }"
						class="tabs">
					<div slot="1">
						<span style="font-size: 15px">{{ t('EVENTS') }}:</span>
					</div>
					<div slot="2">
						<img src="@/assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="3">
						<img src="@/assets/threeBarsHIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
					<div slot="4">
						<img src="@/assets/calendarIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
				</tabs>
			</div>
			<events-map class="viewer" v-show="selectedTab==2" @openEventModal="openEventModal()" :events="events"
					:selectedEventId="selectedEventId" :key="selectedEventId" :scrip="scrip" ref="eventsMap"
					:store="store"/>
			<events-list class="viewer" v-show="selectedTab==3" @openEventModal="openEventModal()" :events="events"
					:store="store"/>
			<events-calendar class="viewer" v-show="selectedTab==4" @openEventModal="openEventModal()" :events="events"
					:store="store"/>
			<div style="font-size: 20px; margin-bottom: 10px;" v-if="!isAuthenticatedUser">
				{{ t('REACH OUT TO NEW HORIZONS') }}
			</div>
			<div style="font-size: 20px; margin-bottom: 10px;" v-else>
				{{ t('WELCOME') }}&nbsp;{{ store.user.display_name }}
			</div>
		</div>
		<!--modal v-if="showCookiesModal" @closeModals="closeCookiesModal()">
			<div slot="contents" class="cookiesModal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="closeCookiesModal()" class="no-border-button">
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
		<event v-if="showEventModal" @goToMap="goToMap()" :id="selectedEventId" @closeModals="closeEventModal()"/>
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
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
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
				selectedTab: 2,
				showEventModal: Boolean(this.$route.params.id),
				selectedEventId: null,
				events: null,
				loaded: false,
				scrip: document.createElement('script'),
			}
		},
		computed : {
			isAuthenticatedUser () { return functions.isAuthenticatedUser }
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
			this.events = await apiFunctions.getAllEvents()
			let apiKey = await apiFunctions.secretsApiFunction('google_maps_api_key')
			this.scrip.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
			this.scrip.async = true
			this.loaded = true
			this.$emit('endLoading')
		},
		mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				await apiFunctions.updateUserAlerts('Show Cookies')
			},
			openEventModal (id) {
				functions.setBackButtonToCloseModal(this, window, this.closeEventModal)
				this.selectedEventId = id
				this.showEventModal = true
			},
			closeEventModal () {
				// after closing, it goes to the previously opened event in map. should it also scroll to previously
				// opened event in the list and calendar?
				functions.freeUpBackButton(this)
				this.$refs.eventsMap.initMap()
				this.showEventModal = false
			},
			goToMap () {
				this.$refs.eventsMap.initMap()
				this.selectedTab = 2
				this.showEventModal = false
			},
		} // methods
	} // export
</script>
<style scoped>
	.viewer {
		width: 100%;
		height: 100%;
		margin-bottom: 5px;
		border: 2px solid rgba(255, 255, 255, .1);
		border-bottom-left-radius: 7px;
		border-bottom-right-radius: 7px;
	}
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
