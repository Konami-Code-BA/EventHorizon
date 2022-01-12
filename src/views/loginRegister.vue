<template>
	<div class="main" style="justify-content: center;">
		<div style="width: 80%">
			<div style="font-size: 24px; align-self: flex-start">{{ t('LOGIN WITH EMAIL') }}</div>
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
				{{ t('LOGIN WITH EMAIL') }}
			</button>
			<br>
			<div style="width: 100%; display: flex; flex-direction: column; justify-content: center;">
				<button class="link-button" v-on:click.prevent="resetPassword()">
					Forgot Password
				</button>
			</div>
			<!--button class="no-border-button small-button" v-on:click.prevent="sendEmail()">
				<small><small>{{t('FORGOT PASSWORD')}}</small></small>
			</button-->
			<div class="line-height"/>
			<div class="line-height"/>
			<div class="line-height"/>
			<button v-on:click.prevent="goToPage({ page: 'registerWithEmail', args: {} })" class="button">
				{{t('REGISTER EMAIL')}}
			</button>
			<div class="line-height"/>
			<button v-on:click.prevent="loginByLine()" class="button line-coloring" style="display: flex; flex-direction: row; align-items: center; justify-items: center;">
				<img src="@/assets/line.png" style="height: 27px;">
				<div>
					&nbsp;{{t('LINE LOGIN / REGISTER')}}
				</div>
			</button>
		</div>
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'loginRegister',
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
			f.focusCursor(document, 'email')
		},
		watch: {
			'passwordInput' () { this.passwordHasErrors() },
			'emailInput' () { this.emailHasErrors() },
		},
		methods: {
			t (w) { return translations.t(w) },
			goToPage (pageDict) {
				f.goToPage(pageDict)
			},
			async login () {
				if (this.passwordError.length > 0 || this.emailError.length > 0) {
					this.shakeFunction()
					return
				}
				this.showPassword = false
				this.store.loading = true
				let user = await api.login({'email': this.emailInput, 'password': this.passwordInput})
				if (!user.error) {
					f.goToPage(this.store.lastNonLoginRegisterPage)
					window.initMap()
					this.store.loading = false
				} else if (user.error === 'This email is not registered') {
					this.emailError = user.error
				} else if (user.error === 'Incorrect password') {
					this.passwordError = user.error
				}
			},
			showButton () {
				f.focusCursor(document, 'password')
				this.showPassword = !this.showPassword
			},
			async sendEmail() {
				await api.sendEmail()
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
				} else if (f.hasInvalidEmailStructure(this.emailInput) || f.hasIllegalSymbols(this.emailInput)) {
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
			shakeFunction () {
				this.shakeIt = true
				setTimeout(() => { this.shakeIt = false; }, 1000)
			},
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginByLine () {
				this.store.loading = true
				let loginChannelId = await api.secretsApi('login-channel-id')
				let state = await api.secretsApi('new-random-secret')
				document.cookie = `state=${state}; path=/`
				let lineLoginRedirectUrl = 'https%3A%2F%2Fwww.eventhorizon.vip'
				if (process.env.PYTHON_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080'
				} else if (process.env.PYTHON_ENV == '"test"') {
					lineLoginRedirectUrl = 'https%3A%2F%2Fevent-horizon-test.herokuapp.com'
				}
				lineLoginRedirectUrl += f.createUriForReturnFromLogin(f.currentPage, this.store.lastNonLoginRegisterPage, true)
				window.location.replace(`https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive&scope=profile%20openid`)
			},
			async tryLineNewDevice () {
				if (f.currentPage && f.currentPage.args.code && this.stateCookie === f.currentPage.args.state) {
					let nextPage = f.createNextPageFromCurrentPage(f.currentPage)
					let uri = f.createUriForReturnFromLogin(f.currentPage, nextPage, false)
					await api.lineNewDevice(f.currentPage.args.code, uri)
					f.goToPage(nextPage)
				}
			},
			resetPassword () {
				f.goToPage({ page: 'resetPassword', args: {} })
			},
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
	.button {
		width: 100%;
	}
</style>
