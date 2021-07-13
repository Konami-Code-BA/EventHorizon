<template>
	<div>
		<div v-if="!loading">
			<menus-header @logoutLoading="loading=true"/>
			<div class="box">
				<h1>{{ t('HOME') }}</h1>
				<h2>{{ store.user.display_name }}</h2>
				<div style="display: flex; align-items: center; color:grey"><h2>{{ t('UPCOMING EVENTS') }}</h2><small>　({{ t('COMING SOON') }})</small></div>
				<div style="display: flex; align-items: center; color:grey"><h2>{{ t('MY EVENTS') }}</h2><small>　({{ t('COMING SOON') }})</small></div>
				<div style="display: flex; align-items: center; color:grey"><h2>{{ t('TBA') }}</h2><small>　({{ t('COMING SOON') }})</small></div>
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="loading" v-else></div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'home',
		components: {
			menusHeader,
			modal,
		},
		data () {
			return {
				store: store,
				loading: true,
			}
		},
		async mounted () {
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
</style>
