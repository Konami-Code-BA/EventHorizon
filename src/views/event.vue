<template>
	<div class="main">
		<h1>Event</h1>
	</div>
</template>
<script>
	import store from '@/store.js'
	import appHeader from '@/components/appHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'event',
		components: {
			appHeader,
			modal,
		},
		data () {
			return {
				store: store,
			}
		},
		async mounted () {
			this.$emit('endLoading')
			console.log('RECEIVING QUERY', this.$route.query.id)
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
