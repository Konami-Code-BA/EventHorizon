<template>
	<div id="map_canvas" style="width: 100%; height: 100%"/>
</template>
<script>
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'googleMap',
		data () {
			return {
			}
		},
		components: {
		},
		props: {
			events: { default: null },
			selectedEventId: { default: null },
		},
		computed: {
		},
		async mounted () {
			let apiKey = await apiFunctions.secretsApiFunction('google_maps_api_key')
			let script = document.createElement('script')
			script.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
			script.async = true
			document.head.appendChild(script)
			window.initMap = this.initMap
			window.openEventModal = this.openEventModal
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
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
				let markers = {}
				let infowindowContents = []
				for (let i = 0; i < this.events.length; i++) {
					let dateTime = Date.parse(this.events[i]['date_time'])
					if (dateTime < Date.now()) {
						this.events.splice(i, 1)
						i--
					}
				}
				if (this.events.length != 0) {
					console.log('length', this.events.length)
					for (let i = 0; i < this.events.length; i++) {
						let address = this.events[i]['address']
						let geocoder = new google.maps.Geocoder()
						var result
						await geocoder.geocode( { 'address': address }, function(results, status) {
							if (status == google.maps.GeocoderStatus.OK) {
								result = results[0]
							} else {
								alert(' Geocode was not successful for the following reason: ' + status)
							}
						})
						let [randLat, randLng] = [0, 0]
						let icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
						let eventName = 'PRIVATE EVENT'
						if (this.events[i]['is_private']) {
							let randSign = Math.random() > .5 ? 1 : -1
							randLat = Math.random() / 250 * randSign
							randSign = Math.random() > .5 ? 1 : -1
							randLng = Math.random() / 300 * randSign
							icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
							console.log(i, this.events[i]['name'])
						} else {
							eventName = this.events[i]['name']
						}
						infowindowContents.push(`
							<button
								onclick="openEventModal(${this.events[i]['id']})"
								style="
									text-decoration: none;
									color: blue;
									font-weight: 600;
									font-size: 16px;
									-webkit-font-smoothing: antialiased;
									-moz-osx-font-smoothing: grayscale;
									border: none;
									outline: none;
								"
							>
								${eventName}
							</button>
						`)
						let position = new google.maps.LatLng(
							result.geometry.location.lat() + randLat,
							result.geometry.location.lng() + randLng
						)
						let marker = new google.maps.Marker({
							position: position,
							map: map,
							icon: icon
						})
						markers[this.events[i]['id']] = marker
						google.maps.event.addListener(marker, 'click', function() {
							infowindow.setContent(infowindowContents[i])
							infowindow.open(map, this)
						})
						google.maps.event.addListener(map, "click", function() {
							infowindow.close()
						})
						map.setZoom(12)
						bounds.extend(position)
						map.fitBounds(bounds)
					}
				} else {
					let address = '東京都千代田区千代田１−1'
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
					let position = new google.maps.LatLng(
						result.geometry.location.lat() + randLat,
						result.geometry.location.lng() + randLng
					)
					let marker = new google.maps.Marker({
						position: position,
						map: map,
						icon: 'http://maps.google.com/mapfiles/ms/icons/empty.png',
						label: {
							color: 'rgba(0, 0, 0, 0.7)',
   							//highlight: 'rgba(0, 0, 0, 0.5)',
							fontWeight: 'bold',
							text: this.t('NO EVENTS'),
							fontSize: '40px',
						},
					})
					bounds.extend(position)
					map.fitBounds(bounds)
					map.setZoom(12)
				}
				var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
					google.maps.event.removeListener(boundsListener)
				})
				if (this.selectedEventId) {
					map.panTo(markers[this.selectedEventId].getPosition())
					google.maps.event.trigger(markers[this.selectedEventId], 'click');
					map.setZoom(14)
				}
			},
			openEventModal (id) {
				this.$emit('openEventModal', id)
			},
		}
	}
</script>
<style scoped>
	.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
		text-decoration: none;
	}
</style>