<template>
	<div>
		<div class="main">
			<div>
				<img src="../assets/eventhorizonLogo.png" style="max-width: 200px; max-height: 200px;">
			</div>
			<div style="font-size: 38px; margin-bottom: 5px;">EVENT HORIZON</div>
			<div style="width: 100%;">
				<tabs :num-tabs="4" :not-buttons="[1]" :initial="2" @on-click="selectedTab = $event" style="background-color: rgba(0, 0, 0, .2);">
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
			<google-map class="viewer" v-show="selectedTab==2"/>
			<events-calendar class="viewer" v-show="selectedTab==3"/>
			<div style="font-size: 20px; margin-bottom: 10px;">
				{{ t('REACH OUT TO NEW HORIZONS') }}
			</div>
		</div>
		<transition name="fade">
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
		</transition>
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
	export default {
		name: 'experiment1',
		components: {
			modal,
			tabs,
			googleMap,
			eventsCalendar,
		},
		data () {
			return {
				store: store,
				showCookiesModal: store.user.alerts.includes(1),
				selectedTab: 2,
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				await apiFunctions.updateUserAlerts('Show Cookies')
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
