<template>
	<div class="main" style="justify-content: center">
		<button v-on:click.prevent="$router.push({ name: 'loginWithEmail' })" class="button">{{t('LOGIN WITH EMAIL')}}</button>
		<div class="line-height"></div>
		<button v-on:click.prevent="$router.push({ name: 'registerWithEmail' })" class="button">{{t('REGISTER WITH EMAIL')}}</button>
		<div class="line-height"></div>
		<button v-on:click.prevent="loginByLine()" class="button line-coloring">
			<div class="line-button">
				<div class="line-alignment">
					<div>
						<img src="@/assets/line.png" class="line-img">
					</div>
					<div>
						LINE
					</div>
				</div>
			</div>
		</button>
	</div>
</template>
<script src="https://www.line-website.com/social-plugins/js/thirdparty/loader.min.js" async="async" defer="defer"></script>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'loginRegister',
		components: {
		},
		data () {
			return {
				store: store,
				stateCookie: JSON.parse('{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}')['state']
			}
		},
		//compute: {
		//	cookiesString () {

		//	}
		//},
		async mounted () {
			await this.tryLineNewDevice()
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginByLine () {
				this.$emit('startLoading')
				let loginChannelId = await apiFunctions.secretsApi('login-channel-id')
				let state = await apiFunctions.secretsApi('new-random-secret')
				document.cookie = `state=${state}; path=/`
				let lineLoginRedirectUrl = 'https%3A%2F%2Fwww.eventhorizon.vip%2FloginRegister'
				if (process.env.PYTHON_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080%2FloginRegister'
				} else if (process.env.PYTHON_ENV == '"test"') {
					lineLoginRedirectUrl = 'https%3A%2F%2Fevent-horizon-test.herokuapp.com%2FloginRegister'
				}
				window.location.replace(`https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive&scope=profile%20openid`)
			},
			async tryLineNewDevice () {
				if (this.$route.query.code && this.stateCookie === this.$route.query.state) {
					this.$emit('startLoading')
					await apiFunctions.lineNewDevice(this.$route.query.code, 'loginRegister')
					this.$emit('endLoading')
					this.$router.push({ name: 'events' })
				}
			}
		} // methods
	} // export
</script>
<style scoped>
	.line-coloring {
		background-color: #00b300;
		color: white;
		padding: 0;
		border-color: #00b300;
	}
	.line-alignment {
		display: flex;
		flex-direction: row;
		align-items: center;
		width: 90px;
		justify-content: space-between;
		height: inherit !important;
	}
	.line-img {
		height: 27px;
		transform: translate(0, 2px);
	}
	.button {
		width: 80%;
	}
</style>
