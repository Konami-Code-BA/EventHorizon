<template>
	<div class="main">
		<form v-on:keyup.enter="login()">
			<div>
				<input :placeholder="t('EMAIL')" v-model="emailInput" type="text"
					id="email" autocorrect="off" autocapitalize="none"/>
			</div>
			<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(emailError)}}</small>
			</div>
			<div style="display: flex">
				<input :placeholder="t('PASSWORD')" v-model="passwordInput"
					:type="[showPassword ? 'text' : 'password']" style="flex-grow: 1"
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
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
<script>
	import store from '@/store.js'
	import appHeader from '@/components/appHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'loginWithEmail',
		components: {
			appHeader,
			modal,
		},
		data () {
			return {
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
			this.passwordHasErrors()
			this.emailHasErrors()
			this.$emit('endLoading')
			functions.focusCursor('email')
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
					this.$router.push({ name: 'home' })
				} else if (error === 'This email is not registered') {
					this.emailError = error
				} else if (error === 'Incorrect password') {
					this.passwordError = error
				}
			},
			showButton () {
				functions.focusCursor('password')
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
				let symbols = '`~!#$%^&*()+=[{]}\\|;:\'",<>/?'
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
			//goToPage2 () {
			//	this.$router.push({ name: 'pageTwo', params: { thruParams: 'this was sent from the login page' } })
			//},
		} // methods
	} // export
</script>
<style scoped>
</style>
