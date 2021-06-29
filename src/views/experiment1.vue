<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<h1>experiment 1</h1>
				<div><h2>{{$route.query.test}}</h2></div> <!--http://127.0.0.1:8080/experiment1?test=boi-->
				<button v-on:click.prevent="sendEmail()">sendEmail</button>
				<button v-on:click.prevent="sendWebhook()">sendWebhook</button>
				<button v-on:click.prevent="lineConsumption()">lineConsumption</button>
				<button v-on:click.prevent="linePush()">linePush</button>
				<button v-on:click.prevent="lineBroadcast()">lineBroadcast</button>
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
		name: 'experiment1',
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
        	//setTimeout(() => { }, 2000)
			this.loading = false
			
		},
		methods: {
			t (w) { return translations.t(w) },
			async sendEmail () { await apiFunctions.sendEmail() },
			async sendWebhook () { await apiFunctions.sendWebhook() },
			async lineConsumption () { await apiFunctions.lineConsumption() },
			async linePush () { await apiFunctions.linePush() },
			async lineBroadcast () { await apiFunctions.lineBroadcast() },
		} // methods
	} // export
</script>
<style scoped>
</style>
