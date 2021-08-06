<template>
	<div id="map_canvas" style="width: 100%; height: 100%"/>
</template>
<script>
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
			this.$emit('endLoading')
		},
		methods: {
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
		}
	}
</script>
<style scoped>
	.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
		text-decoration: none;
	}
</style>