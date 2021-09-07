<template>
	<div v-if="loaded">
		<div class="main" v-show="!showEventModal">
			<div>
				<img src="../assets/eventhorizonLogo.png" style="max-width: 200px; max-height: 200px;">
			</div>
			<div style="font-size: 38px; margin-bottom: 5px;">EVENT HORIZON</div>
			<div style="width: 100%;">
				<tabs :num-tabs="4" :not-buttons="[1]" :initial="selectedTab" :key="selectedTab"
						@on-click="selectedTab = $event" style="background-color: rgba(0, 0, 0, .2);">
					<div slot="1">
						<span style="font-size: 15px">{{ t('EVENTS') }}:</span>
					</div>
					<div slot="2">
						<img src="../assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="3">
						<img src="../assets/calendarIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
					<div slot="4">
						<img src="../assets/threeBarsHIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
				</tabs>
			</div>
			<google-map class="viewer" v-show="selectedTab==2" @openEventModal="openEventModal" :events="events"
					:selectedEventId="selectedEventId" :key="selectedEventId"/>
			<events-calendar class="viewer" v-show="selectedTab==3" @openEventModal="openEventModal" :events="events"/>
			<div style="font-size: 20px; margin-bottom: 10px;">
				{{ t('REACH OUT TO NEW HORIZONS') }}
			</div>
		</div>
		<modal v-show="showCookiesModal" @closeModals="closeCookiesModal()">
			<div slot="contents" class="cookiesModal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="closeCookiesModal()" class="no-border-button">
						✖
					</button>
				</div>
				<div style="white-space: pre-line; text-align: center; font-weight: 400;">
					{{t('This site uses cookies')}}
				</div><br>
				<div style="text-align: center">
					<button v-on:click.prevent="closeCookiesModal()" class="button" style="width: 100%">
						<big>{{t('OK')}}</big>
					</button>
				</div><br><br>
			</div>
		</modal>
		<event v-if="showEventModal" @goToMap="showEventModal = false; selectedTab = 2" :id="selectedEventId"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import tabs from '@/components/tabs.vue'
	import googleMap from '@/components/googleMap.vue'
	import eventsCalendar from '@/components/eventsCalendar.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import event from '@/components/event.vue'
	export default {
		name: 'experiment1',
		components: {
			modal,
			tabs,
			googleMap,
			eventsCalendar,
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
			}
		},
		watch: {
			'showEventModal' () {
				if (!this.showEventModal && this.$route.params.id) {
					this.$router.push({ name: 'front' })
				}
			},
		},
		async created () {
			this.events = await apiFunctions.getAllEvents()
			this.loaded = true
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
				this.selectedEventId = id
				this.showEventModal = true
			},
		} // methods
	} // export
</script>
<style scoped>
	.viewer {
		width: 100%;
		height: 100%;
		margin-bottom: 5px;
		border: 1px solid rgba(255, 255, 255, .1);
	}
</style>
