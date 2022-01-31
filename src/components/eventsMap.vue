<template>
	<div id="map_canvas" style="width: 100%; height: 100%"/>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'eventsMap',
		data () {
			return {
				store: store,
			}
		},
		components: {
		},
		watch: {
			'store.user.language' () {
				window.initMap()
			},
		},
		async created () {
		},
		async mounted () {
			window.initMap = this.initMap
			window.openEventModal = this.openEventModal
			window.initMap()
		},
		methods: {
			t (w) { return translations.t(w) },
			async initMap () {
				try {
					let map = new google.maps.Map(document.getElementById("map_canvas"), {
						mapTypeId: 'roadmap',
						streetViewControl: false,
						clickableIcons: false,
						controlSize: 30,
						tilt: 45,
						disableDefaultUI: true,
						zoom: 12,
						styles: [
							{ elementType: "geometry", stylers: [{ color: "#242f3e" }] },
							{ elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
							{ elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
							{
								featureType: "administrative.locality",
								elementType: "labels.text.fill",
								stylers: [{ color: "#d59563" }],
							}, {
								featureType: "poi",
								elementType: "labels.text.fill",
								stylers: [{ color: "#d59563" }],
							}, {
								featureType: "poi.park",
								elementType: "geometry",
								stylers: [{ color: "#263c3f" }],
							}, {
								featureType: "poi.park",
								elementType: "labels.text.fill",
								stylers: [{ color: "#6b9a76" }],
							}, {
								featureType: "road",
								elementType: "geometry",
								stylers: [{ color: "#38414e" }],
							}, {
								featureType: "road",
								elementType: "geometry.stroke",
								stylers: [{ color: "#212a37" }],
							}, {
								featureType: "road",
								elementType: "labels.text.fill",
								stylers: [{ color: "#9ca5b3" }],
							}, {
								featureType: "road.highway",
								elementType: "geometry",
								stylers: [{ color: "#746855" }],
							}, {
								featureType: "road.highway",
								elementType: "geometry.stroke",
								stylers: [{ color: "#1f2835" }],
							}, {
								featureType: "road.highway",
								elementType: "labels.text.fill",
								stylers: [{ color: "#f3d19c" }],
							}, {
								featureType: "transit",
								elementType: "geometry",
								stylers: [{ color: "#2f3948" }],
							}, {
								featureType: "transit.station",
								elementType: "labels.text.fill",
								stylers: [{ color: "#d59563" }],
							}, {
								featureType: "water",
								elementType: "geometry",
								stylers: [{ color: "#17263c" }],
							}, {
								featureType: "water",
								elementType: "labels.text.fill",
								stylers: [{ color: "#515c6d" }],
							}, {
								featureType: "water",
								elementType: "labels.text.stroke",
								stylers: [{ color: "#17263c" }],
							},
						],
					})
					let bounds = new google.maps.LatLngBounds()
					let infowindow = new google.maps.InfoWindow({ map: map })
					let markers = {}
					let infowindowContents = []
					let noEvents = true
					if (this.store.events.display.length != 0) {
						for (let i = 0; i < this.store.events.display.length; i++) {
							if (this.store.events.display[i].latitude != 0
									|| this.store.events.display[i].longitude != 0) {
								noEvents = false
								let icon = window.origin.replace('8080', '8000') + '/static/publicPastMapIcon.png'
								if (f.isoStringDateToDateObject(this.store.events.display[i].date_time) > f.today) {
									icon = window.origin.replace('8080', '8000') + '/static/publicMapIcon.png'
								}
								if (this.store.events.display[i].is_private
										&& !f.isGuestStatus(this.store.events.display[i], 'invited')) {
									if (f.isoStringDateToDateObject(this.store.events.display[i].date_time) > f.today) {
										icon = window.origin.replace('8080', '8000') + '/static/privateMapIcon.png'
									} else {
										icon = window.origin.replace('8080', '8000') + '/static/privatePastMapIcon.png'
									}
								} else if (f.isGuestStatus(this.store.events.display[i], 'invited')) {
									if (f.isoStringDateToDateObject(this.store.events.display[i].date_time) > f.today) {
										icon = window.origin.replace('8080', '8000') + '/static/myMapIcon.png'
									} else {
										icon = window.origin.replace('8080', '8000') + '/static/myPastMapIcon.png'
									}
								}
								infowindowContents.push(`
									<button
										onclick="openEventModal(${this.store.events.display[i].id})"
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
										${this.store.events.display[i].name}
									</button>
								`)
								let position = new google.maps.LatLng(
									this.store.events.display[i].latitude,
									this.store.events.display[i].longitude
								)
								let image = new google.maps.MarkerImage(
									icon, null, null, null, new google.maps.Size(35, 35)
								)
								let marker = new google.maps.Marker({
									position: position,
									map: map,
									icon: image,
								})
								markers[this.store.events.display[i].id] = marker
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
						let position = new google.maps.LatLng(
							35.685174,
							139.752744
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
					if (markers[this.selectedEventId]) {
						bounds.extend(markers[this.selectedEventId].getPosition())
						await map.fitBounds(bounds)
						map.setZoom(15)
						map.panTo(markers[this.selectedEventId].getPosition())
						google.maps.event.trigger(markers[this.selectedEventId], 'click');
					}
					var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
						google.maps.event.removeListener(boundsListener)
					})
				} catch (error) { }
			},
			openEventModal (id) {
				f.goToPage({ page: 'event', args: { id: id } })
			},
		}
	}
</script>
<style scoped>
	.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
		text-decoration: none;
	}
</style>