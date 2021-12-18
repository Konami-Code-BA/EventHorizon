<template>
	<div class="main">
		<div style="font-size: 36px">{{ t('ME') }}</div>
		<div class="line-height"></div>
		<div style="font-size: 24px">{{ store.user.display_name }}</div>
		<div class="line-height"></div>
		<div style="color: grey">({{ t('COMING SOON') }})</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	export default {
		name: 'profile',
		components: {
		},
		data () {
			return {
				store: store,
				displayName: '',
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
