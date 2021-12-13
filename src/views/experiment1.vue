<template>
	<div>
		<div class="main">
			<div>
				<img src="@/assets/eventhorizonLogo.png" style="max-width: 200px; max-height: 200px;">
			</div>
			<div style="font-size: 32px; margin-bottom: 10px;">EVENT HORIZON</div>
			<div style="width: 100%;">
				<tabs :tab-no="4">
					<div slot="1">
						<span style="font-size: 20px; white-space: pre-line; margin-bottom: 10px;">{{ t('EVENTS') }}:</span>
					</div>
					<div slot="2">
						<img src="@/assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="3">
						<img src="@/assets/calendarIcon.png" class="icon"/>
					</div>
					<div slot="4">
						<img src="@/assets/threeBarsHIcon.png" class="icon"/>
					</div>
				</tabs>
			</div>
			<div id="map_canvas" style="width: 100%; height: 100%;"></div>
			<div style="font-size: 20px; white-space: pre-line; margin-bottom: 10px;">{{ t('REACH OUT TO NEW HORIZONS') }}</div>
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
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import tabs from '@/components/tabs.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'experiment1',
		components: {
			modal,
			tabs,
		},
		data () {
			return {
				store: store,
				showCookiesModal: store.user.alerts.includes(1),
			}
		},
		async mounted () {
        	//setTimeout(() => { }, 2000)
			let apiKey = await apiFunctions.secretsApiFunction('google_maps_api_key')
			let script = document.createElement('script')
			script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`
			script.async = true
			document.head.appendChild(script)
			window.initMap = this.initMap
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				await apiFunctions.updateUserAlerts('Show Cookies')
			},
			async initMap () {
				let bounds = new google.maps.LatLngBounds()
				let map = new google.maps.Map(
					document.getElementById("map_canvas"),
					{
						mapTypeId: 'roadmap',
      					streetViewControl: false,
						clickableIcons: false,
						controlSize: 30,
						tilt: 45,
					})
				let infowindow = new google.maps.InfoWindow({ map: map })
				let events = await apiFunctions.getAllEvents()
				for ( let i = 0; i < events.length; i++) {
					let dateTime = Date.parse(events[i]['date_time'])
					if (dateTime < Date.now()) {
						continue
					}
					let address = events[i]['address']
					let geocoder = new google.maps.Geocoder()
					var result
					await geocoder.geocode( { 'address': address }, function(results, status) {
						if (status == google.maps.GeocoderStatus.OK) {
							result = results[0]
						} else {
							alert('Geocode was not successful for the following reason: ' + status)
						}
					})
					let [randLat, randLng] = [0, 0]
					let icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
					let styles = `style="
						text-decoration: none;
						color: blue;
						font-weight: 600;
						font-size: 16px;
						-webkit-font-smoothing: antialiased;
						-moz-osx-font-smoothing: grayscale;
					"`
					let infowindowContents = '<a '
						+ 'href="' + apiFunctions.apiBaseUrl + '/event/?id=' + events[i]['id'] + '"' + styles + '>'
						+ events[i]['name'] + '</a>'
					if (events[i]['is_private']) {
						let randSign = Math.random() > .5 ? 1 : -1
						randLat = Math.random() / 250 * randSign
						randSign = Math.random() > .5 ? 1 : -1
						randLng = Math.random() / 300 * randSign
						icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
						infowindowContents = '<span ' + styles + '>' + events[i]['name'] + '</span>'
					}
					let position = new google.maps.LatLng(
						result.geometry.location.lat() + randLat,
						result.geometry.location.lng() + randLng
					)
					let marker = new google.maps.Marker({
						position: position,
						map: map,
						icon: icon
					})
					google.maps.event.addListener(marker, 'click', function() {
						infowindow.setContent(infowindowContents)
						infowindow.open(map, this)
					})
					google.maps.event.addListener(map, "click", function() {
						infowindow.close()
					})
					bounds.extend(position)
					map.fitBounds(bounds)
				}
				var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
					google.maps.event.removeListener(boundsListener)
				})
			}
		} // methods
	} // export
</script>
<style scoped>
.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
  text-decoration: none;
}
</style>
