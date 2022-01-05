<template>
	<div class="main">
		urls
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	export default {
		name: 'urlDisplay',
		components: {
		},
		data () {
			return {
				store: store,
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
