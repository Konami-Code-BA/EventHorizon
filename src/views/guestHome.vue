<template>
	<div>
		<div class="box">
			<div class="box-item" style="font-size: 36px;">{{ t('HOME') }}</div>
			<div class="box-height"></div>
			<div class="box-item" style="font-size: 24px;">{{ store.user.display_name }}</div>
			<div class="box-height"></div>
			<div class="box-item coming-soon-list"><div style="font-size: 16px;">{{ t('UPCOMING EVENTS') }}</div><small>({{ t('COMING SOON') }})</small></div>
			<div class="box-height"></div>
			<div class="box-item coming-soon-list"><div style="font-size: 16px;">{{ t('MY EVENTS') }}</div><small>({{ t('COMING SOON') }})</small></div>
			<div class="box-height"></div>
			<div class="box-item coming-soon-list"><div style="font-size: 16px;">{{ t('TBA') }}</div><small>({{ t('COMING SOON') }})</small></div>
		</div>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
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
		name: 'home',
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
	align-items: center;
	justify-content: space-between;
	color: grey;
}
</style>
