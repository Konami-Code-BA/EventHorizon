<template>
	<div class="main">
		<div style="font-size: 36px;">PEOPLE</div>
		<div class="line-height"></div>
		<div style="font-size: 24px;">{{ store.user.display_name }}</div>
		<div class="line-height"></div>
		<div class="coming-soon-list"><div style="font-size: 16px;">{{ t('UPCOMING EVENTS') }}</div><small>({{ t('COMING SOON') }})</small></div>
		<div class="line-height"></div>
		<div class="coming-soon-list"><div style="font-size: 16px;">{{ t('MY EVENTS') }}</div><small>({{ t('COMING SOON') }})</small></div>
		<div class="line-height"></div>
		<div class="coming-soon-list"><div style="font-size: 16px;">{{ t('TBA') }}</div><small>({{ t('COMING SOON') }})</small></div>
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
		name: 'profile',
		components: {
			appHeader,
			modal,
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
.coming-soon-list {
	display: flex;
	flex-direction: row;
	align-items: center;
	justify-content: space-between;
	width: 100%;
	color: grey;
}
</style>
