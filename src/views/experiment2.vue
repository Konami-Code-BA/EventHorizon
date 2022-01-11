<template>
	<div>
		<div class="main">
			<h1>experiment 2</h1>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'experiment2',
		components: {
		},
		data () {
			return {
				store: store,
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
