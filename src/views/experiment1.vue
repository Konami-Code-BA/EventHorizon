<template>
	<div>
		<div class="main" id="page">
			some stuff
			<button v-on:click.prevent="trything2()">trything</button>
		</div>
	</div>
</template>
<script>
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'experiment1',
		components: {
		},
		data () {
			return {
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			//trything1 () {
			//	require('html2canvas')(document.querySelector("#page"))
			//		.then(canvas => {
			//			canvas.toBlob(function(blob) {
			//				console.log(typeof blob)
			//				saveAs(blob, "Dashboard.png");
			//			})
			//		})
			//},
			async trything2 () {
				await apiFunctions.createEvent({
					name: 'name',
					description: 'description',
					address: '〒160-0023 東京都新宿区西新宿３丁目２−9',
					venue_name: 'venue_name',
					latitude: 0,
					longitude: 0,
					date_time: new Date(),
					include_time: true,
					is_private: false,
					hosts: [387],
					guests: [387],
					confirmed_guests: [387],
					interested_guests: [387],
					invited_guests: [387],
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
