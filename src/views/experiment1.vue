<template>
	<div>
		<div class="main" id="page">
			some stuff
			<button v-on:click.prevent="trything()">trything</button>
		</div>
	</div>
</template>
<script>
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
			trything () {
				require('html2canvas')(document.querySelector("#page"))
					.then(canvas => {
						canvas.toBlob(function(blob) {
							console.log(typeof blob)
							saveAs(blob, "Dashboard.png");
						})
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
