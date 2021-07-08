<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<div style="display: flex; width: 100%">
					<button v-on:click.prevent="$router.push(name='loginByEmail')" class="box-item" style="flex-grow: 1">Login With Email</button>
					<button v-on:click.prevent="$router.push(name='registerByEmail')" class="box-item" style="flex-grow: 1">Register With Email</button>
				</div>
				<div class="box-item"></div>
					<button v-on:click.prevent="loginByLine()" class="box-item line" style="flex-grow: 1">
					<div style="display: flex; height: 100%; width: 70px; align-items: center; justify-content: space-between;">
						<img src="../assets/line.png" style="height: inherit">
						<div>Line</div>
					</div>
					</button>
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
				loading: true,
				stateCookie: JSON.parse('{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}')['state']
			}
		},
		//compute: {
		//	cookiesString () {

		//	}
		//},
		async mounted () {
			console.log('code', this.$route.query.code)
			console.log('friendship_status_changed', this.$route.query.friendship_status_changed)
			console.log('state', this.$route.query.state)
			console.log('error', this.$route.query.error)
			console.log('error_description', this.$route.query.error_description)
			this.tryLineNewDevice()
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginChannelId () {
				let response = await apiFunctions.loginChannelId()
				return response
			},
			async state () {
				let response = await apiFunctions.state()
				return response
			},
			async loginByLine () {
				let loginChannelId = await apiFunctions.loginChannelId()
				let state = await apiFunctions.state()
				document.cookie = `state=${state}`;
				let lineLoginRedirectUrl = 'https%3A%2F%2Fwww.eventhorizon.vip%2FloginRegister'
				if (process.env.NODE_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080%2FloginRegister'
				}
				window.location.replace(`https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive&scope=profile%20openid`)
			},
			async tryLineNewDevice () {
				if (this.$route.query.code && this.stateCookie === this.$route.query.state) {
					await apiFunctions.lineNewDevice(this.$route.query.code)
					this.$router.push({ name: 'home' })
				} else {
					console.log('not logged in yet')
				}
			}
		} // methods
	} // export
</script>
<style scoped>
	.line {
		background-color: #00c300;
		color: white;
	}
</style>
