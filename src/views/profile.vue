<template>
	<div class="main">
		<div style="font-size: 36px;">PROFILE</div>
		<div class="line-height"></div>
		<div style="font-size: 24px;">{{ store.user.display_name }}</div>
		<div class="line-height"></div>
		<div class="coming-soon-list">({{ t('COMING SOON') }})</div>
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
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	color: grey;
}
</style>
