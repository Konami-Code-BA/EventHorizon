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
				<button v-on:click.prevent="lineLogin()">lineLogin</button>
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
			async loginChannelId () {
				let response = await apiFunctions.loginChannelId()
				return response
			},
			async state () {
				let response = await apiFunctions.state()
				return response
			},
			async lineLogin () {
				let loginChannelId = await this.loginChannelId()
				let state = await this.state()
				store.state = state
				let lineLoginRedirectUrl = 'http%3A%2F%2Feventhorizon.vip%2Flogin'
				if (process.env.NODE_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080%2Flogin'
				}
				window.location.replace(`https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}&redirect_uri=${lineLoginRedirectUrl}&state=${state}&bot_prompt=aggressive&scope=profile%20openid`)
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
