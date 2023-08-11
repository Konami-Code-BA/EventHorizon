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
				mapStyling: [
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
			}
		},
		components: {
		},
		async created () {
			window.initMap = this.initMap
			window.openEventModal = this.openEventModal
		},
		methods: {
			t (w) { return translations.t(w) },
			infoWindow (i, isInvited, isPast) {
				return `
					<button
						onclick="openEventModal(${this.store.events.display[i].id})"
						style="
							text-decoration: none;
							color: black;
							font-weight: 600;
							font-size: 16px;
							-webkit-font-smoothing: antialiased;
							-moz-osx-font-smoothing: grayscale;
							border: 3px solid ${isInvited ? '#44ff00' : '#ffffff'};
							border-radius: 15px;
							outline: 1px solid #585858;
							margin: 1px;
							background-color: ${isPast ? '#585858' : '#ffffff'} !important;
						"
					>
						${this.store.events.display[i].name}
					</button>
				`
			},
			async initMap () {
				console.log('INIT MAP')
				try {
					let map = new google.maps.Map(document.getElementById("map_canvas"), {
						mapTypeId: 'roadmap',
						streetViewControl: false,
						clickableIcons: false,
						controlSize: 30,
						tilt: 45,
						disableDefaultUI: true,
						styles: this.mapStyling,
					})
					let tokyoBounds = new google.maps.LatLngBounds(
						new google.maps.LatLng(35.58, 139.58), // Southwest corner of Tokyo 23 wards
    					new google.maps.LatLng(35.82, 139.95)  // Northeast corner of Tokyo 23 wards
					)
					let markers = {}
					let infowindowContents = []
					let noEvents = true
					if (this.store.events.display.length != 0) {
						for (let i = 0; i < this.store.events.display.length; i++) {
							if (this.store.events.display[i].latitude != 0
									|| this.store.events.display[i].longitude != 0) {
								noEvents = false
								let isPrivate = this.store.events.display[i].is_private
								let isInvited = f.isGuestStatus(this.store.events.display[i], 'invited')
								let isPast = f.isoStringDateToDateObject(this.store.events.display[i].date_time) <= f.today
								let iconFileName = isPast ? 'past' : 'upcoming'
								iconFileName += isInvited ? 'My' : (isPrivate ? 'Private' : 'Public')
								iconFileName += 'MapIcon2.png'
								let icon = window.origin.replace('8080', '8000') + `/static/${iconFileName}`
								infowindowContents.push(this.infoWindow(i, isInvited, isPast))
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
								let infowindow = new google.maps.InfoWindow({ map: map })
								google.maps.event.addListener(marker, 'click', function() {
									infowindow.close() // close any other open window
									infowindow.setContent(infowindowContents[i])
									infowindow.open(map, this)
								})
								//google.maps.event.trigger(marker, 'click') // auto open all windows
								google.maps.event.addListener(map, "click", function() {
									infowindow.close()
								})
								map.fitBounds(tokyoBounds)
							}
						}
					}
					if (noEvents) {
						console.log('NO EVENTS')
						let position = new google.maps.LatLng(
							35.685174,
							139.752744
						)
						let marker = new google.maps.Marker({
							position: position,
							map: map,
							icon: '',
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
					if (markers[this.selectedEventId]) {
						bounds.extend(markers[this.selectedEventId].getPosition())
						map.fitBounds(bounds)
						map.setZoom(12)
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