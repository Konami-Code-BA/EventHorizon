<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'resetPassword',
		components: {
			modal,
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
