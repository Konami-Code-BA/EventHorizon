<template>
	<div>
		<div v-if="!loading">
			<menus-header @startLoading="loading=true" @endLoading="loading=false"/>
			<div class="box">
				<h1>experiment 1</h1>
				<div id="map_canvas" style="height: 400px; width: 100%;"></div>
			</div>
		</div>
		<div class="loading" v-else></div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'experiment1',
		components: {
			menusHeader,
			modal,
		},
		data () {
			return {
				store: store,
				loading: true,
			}
		},
		async mounted () {
        	//setTimeout(() => { }, 2000)
			let apiKey = await apiFunctions.secretsApiFunction('google_maps_api_key')
			console.log(apiKey)
			let script = document.createElement('script');
			script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`
			script.async = true
			document.head.appendChild(script)




			let markers = [
				['London Eye, London', 51.503454,-0.119562],
				['Palace of Westminster, London', 51.499633,-0.124755]
			];
			this.loading = false
			window.initMap = async function() {
				let address = '〒160-0023 東京都新宿区西新宿３丁目２−9'
  				let geocoder = new google.maps.Geocoder()
				geocoder.geocode( { 'address': address }, function(results, status) {
					if (status == google.maps.GeocoderStatus.OK) {
						let bounds = new google.maps.LatLngBounds()
						let map = new google.maps.Map(document.getElementById("map_canvas"), { mapTypeId: 'roadmap' });
						console.log('LAT', results[0].geometry.location.lat())
						console.log('LNG', results[0].geometry.location.lng())
						let position = results[0].geometry.location
						let marker = new google.maps.Marker({
							position: position,
							map: map,
    						label: '1',
						})
						console.log(marker)
						let thing = 'http://127.0.0.1:8080/experiment2'
						//google.maps.event.addListener(marker, 'click', (function(thing) {
						//	return function() {
						//		window.location.href = thing
						//	}
						//})(thing));
						let infowindow =  new google.maps.InfoWindow({
							content: `<a href="${thing}">Click here</a>`,
							map: map
						})
						google.maps.event.addListener(marker, 'click', function() {
							infowindow.open(map, this);
						})
						google.maps.event.addListener(map, "click", function() {
							infowindow.close();
						});
						map.fitBounds(bounds);
						bounds.extend(position);
						map.setTilt(45);
						//marker.addListener('click', () => { document.$router.push({ name: 'experiment2' }) })
						var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
							this.setZoom(15);
							google.maps.event.removeListener(boundsListener);
						});
					} else {
						alert('Geocode was not successful for the following reason: ' + status);
					}
				})
			}
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
