<template>
	<div id="map_canvas" style="width: 100%; height: 100%"/>
</template>
<script>
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'eventsMap',
		data () {
			return {
			}
		},
		components: {
		},
		props: {
			events: { default: null },
			selectedEventId: { default: null },
			scrip: {},
			store: { default: null },
		},
		computed: {
		},
		async mounted () {
			document.head.appendChild(this.scrip)
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
						disableDefaultUI: true,
					})
				let infowindow = new google.maps.InfoWindow({ map: map })
				let markers = {}
				let infowindowContents = []
				for (let i = 0; i < this.events.length; i++) {
					let dateTime = Date.parse(this.events[i].date_time)
					if (dateTime < Date.now()) {
						this.events.splice(i, 1)
						i--
					}
				}
				let noEvents = true
				if (this.events.length != 0) {
					for (let i = 0; i < this.events.length; i++) {
						if (this.events[i].latitude != 0 || this.events[i].longitude != 0) {
							noEvents = false
							let icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
							if (this.events[i].is_private && !this.isInvitedGuest(this.events[i])) {
								icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
							}
							infowindowContents.push(`
								<button
									onclick="openEventModal(${this.events[i].id})"
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
									${this.events[i].name}
								</button>
							`)
							let position = new google.maps.LatLng(
								this.events[i].latitude,
								this.events[i].longitude
							)
							let marker = new google.maps.Marker({
								position: position,
								map: map,
								icon: icon
							})
							markers[this.events[i].id] = marker
							google.maps.event.addListener(marker, 'click', function() {
								infowindow.close()
								infowindow.setContent(infowindowContents[i])
								infowindow.open(map, this)
							})
							google.maps.event.addListener(map, "click", function() {
								infowindow.close()
							})
							bounds.extend(position)
							await map.fitBounds(bounds)
							map.setZoom(12)
						}
					}
				}
				if (noEvents) {
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
					let position = new google.maps.LatLng(
						result.geometry.location.lat(),
						result.geometry.location.lng()
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
					await map.fitBounds(bounds)
					map.setZoom(12)
				}
				if (this.selectedEventId) {
					bounds.extend(markers[this.selectedEventId].getPosition())
					await map.fitBounds(bounds)
					map.setZoom(15)
					map.panTo(markers[this.selectedEventId].getPosition())
					google.maps.event.trigger(markers[this.selectedEventId], 'click');
				}
				var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
					google.maps.event.removeListener(boundsListener)
				})
			},
			openEventModal (id) {
				this.$emit('openEventModal', id)
			},
			isInvitedGuest (event) {
				return f.isInvitedGuest(event)
			},
		}
	}
</script>
<style scoped>
	.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
		text-decoration: none;
	}
</style>