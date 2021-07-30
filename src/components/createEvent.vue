<template>
	<div class="box">
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registerWithEmailInternal',
		components: {
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
		},
		async mounted () {
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
