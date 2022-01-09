<template>
	<div class="main">
		ABOUT US
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'aboutUs',
		data () {
			return {
			}
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
