<template>
	<div class="main">
		FAQ
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'faq',
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
