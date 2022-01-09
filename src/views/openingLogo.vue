<template>
	<div>
		<div style="font-size: 40px;">
			EVENT HORIZON
		</div>
		<div class="line-height"/>
		<div>
			<img src="@/assets/eventhorizonLogo.png" style="max-width: 250px; max-height: 250px">
		</div>
		<div class="line-height"/>
		<div style="font-size: 20px;">
			{{ t('REACH OUT TO NEW HORIZONS') }}
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'openingLogo',
		components: {
		},
		watch: {
		},
		data () {
			return {
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
