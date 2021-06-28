<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<h1>{{t('HOME')}}</h1>
				<div style="display: flex; align-items: center; color:grey"><h2>{{t('UPCOMING EVENTS')}}</h2><small>　({{t('COMING SOON')}})</small></div>
				<div style="display: flex; align-items: center; color:grey"><h2>{{t('MY EVENTS')}}</h2><small>　({{t('COMING SOON')}})</small></div>
				<div style="display: flex; align-items: center; color:grey"><h2>{{t('TBA')}}</h2><small>　({{t('COMING SOON')}})</small></div>
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
				token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
				client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
				client_id: '1655871760',
				usernameInput: '',
				passwordInput: '',
				showPassword: false,
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
