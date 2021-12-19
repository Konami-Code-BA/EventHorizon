<template>
	<div class="main" style="justify-content: center;">
		<div style="width: 80%">
			<div style="font-size: 24px; align-self: flex-start">{{ t('LOGIN') }}</div>
			<form v-on:keyup.enter="login()">
				<div>
					<input :placeholder="t('EMAIL')" v-model="emailInput" type="text"
						id="email" autocorrect="off" autocapitalize="none" style="width: 100%"/>
				</div>
				<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
					<small>{{t(emailError)}}</small>
				</div>
				<div style="display: flex; flex-direction: row">
					<input :placeholder="t('PASSWORD')" v-model="passwordInput"
						:type="[showPassword ? 'text' : 'password']" style="flex-grow: 1; width: 100%"
						id="password" autocorrect="off" autocapitalize="none"/>
					<button v-on:click.prevent="showButton()" class="button" style="width: 70px"
						id="show" type="button">
						<small v-if="!showPassword">
							{{ t('SHOW') }}
						</small>
						<small v-else>
							{{ t('HIDE') }}
						</small>
					</button>
				</div>
			</form>
			<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(passwordError)}}</small>
			</div>
			<button v-on:click.prevent="login()" class="button">
				{{ t('LOGIN') }}
			</button>
			<!--button class="no-border-button small-button" v-on:click.prevent="sendEmail()">
				<small><small>{{t('FORGOT PASSWORD')}}</small></small>
			</button-->
			<div class="line-height"></div>
			<div class="line-height"></div>
			<div class="line-height"></div>
			<button v-on:click.prevent="$router.push({ name: 'registerWithEmail' })" class="button">
				{{t('NEW USER REGISTRATION')}}
			</button>
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
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
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
				stateCookie: JSON.parse('{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}')['state'],
				store: store,
				emailInput: '',
				shakeIt: false,
				passwordInput: '',
				showPassword: false,
				emailError: '',
				passwordError: '',
			}
		},
		async mounted () {
			await this.tryLineNewDevice()
			this.passwordHasErrors()
			this.emailHasErrors()
			this.$emit('endLoading')
			f.focusCursor(document, 'email')
		},
		watch: {
			'passwordInput' () { this.passwordHasErrors() },
			'emailInput' () { this.emailHasErrors() },
		},
		methods: {
			t (w) { return translations.t(w) },
			async login () {
				if (this.passwordError.length > 0 || this.emailError.length > 0) {
					this.shakeFunction()
					return
				}
				this.showPassword = false
				this.$emit('startLoading')
				let error = await apiFunctions.login({'email': this.emailInput, 'password': this.passwordInput})
				this.$emit('endLoading')
				if (!error) {
					this.$router.push({ name: 'events' })
				} else if (error === 'This email is not registered') {
					this.emailError = error
				} else if (error === 'Incorrect password') {
					this.passwordError = error
				}
			},
			showButton () {
				f.focusCursor(document, 'password')
				this.showPassword = !this.showPassword
			},
			async sendEmail() {
				await apiFunctions.sendEmail()
			},
			passwordHasErrors() {
				if (this.passwordInput.length < 1 ) {
					this.passwordError = 'Required'
					return true
				} else if (this.passwordInput.length < 4) {
					this.passwordError = 'Must be 4 characters or more'
					return true
				} else if (this.passwordInput.length > 75) {
					this.passwordError = 'Must be 75 characters or less'
					return true
				} else {
					this.passwordError = ''
					return false
				}
			},
			emailHasErrors() {
				if (this.passwordError === 'Incorrect password') {
					this.passwordError = ''
				}
				if (this.emailInput.length < 1) {
					this.emailError = 'Required'
					return true
				} else if (this.hasInvalidEmailStructure() || this.hasIllegalSymbols(this.emailInput)) {
					this.emailError = 'This is an impossible email'
					return true
				} else if (this.emailInput.length > 75) {
					this.emailError = 'Must be 75 characters or less'
					return true
				} else {
					this.emailError = ''
					return false
				}
			},
			hasIllegalSymbols (value) {
				let symbols = '`~!#$%^&*()=[{]}\\|;:\'",<>/?'
				for (let i = 0; i < symbols.length; i++) {
					if (value.includes(symbols[i])) {
						return true
					}
				}
				return false
			},
			hasInvalidEmailStructure () {
				let atSplit = this.emailInput.split('@')
				if (atSplit.length != 2) {
					return true
				}
				let [mailPrefix, mailDomain] = atSplit
				let periodSplit = mailDomain.split('.')
				if (periodSplit.length != 2) {
					return true
				}
				let [domainPrefix, domainSuffix] = periodSplit
				if (mailPrefix.length < 1 || domainPrefix.length < 1 || domainSuffix.length < 2) {
					return true
				}
				return false
			},
			shakeFunction () {
				this.shakeIt = true
				setTimeout(() => { this.shakeIt = false; }, 1000);
			},
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginByLine () {
				this.$emit('startLoading')
				let loginChannelId = await apiFunctions.secretsApiFunction('login_channel_id')
				let state = await apiFunctions.secretsApiFunction('new_random_secret')
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
			},
			//goToPage2 () {
			//	this.$router.push({ name: 'pageTwo', params: { thruParams: 'this was sent from the login page' } })
			//},
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
		width: 100%;
	}
</style>
