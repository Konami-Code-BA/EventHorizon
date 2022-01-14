<template>
	<div style="min-width: 235px">
		<form v-on:keyup.enter="emailPassword()">
			<div v-if="action === 'registerWithEmail'">
				<input :placeholder="t('DISPLAY NAME')" v-model="displayNameInput" type="text"
						:id="`displayName+${action}`" autocorrect="off" autocapitalize="none"
						style="width: 100%"/>

				<div class="line-height error-text" :class="{'shake' : shakeIt}">
					{{t(displayNameError)}}
				</div>

			</div>
			<div>
				<input :placeholder="t('EMAIL')" v-model="emailInput" type="email" autocorrect="off"
						autocapitalize="none" :id="`email+${action}`" style="width: 100%"/>
			</div>

			<div class="line-height error-text" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(emailError)}}</small>
			</div>

			<div style="display: flex">
				<input :placeholder="t('PASSWORD')" v-model="passwordInput" :type="[showPassword ? 'text' : 'password']"
						style="flex-grow: 1" :id="`password+${action}`" autocorrect="off" autocapitalize="none"/>
				<button v-on:click.prevent="showButton()" class="button" style="width: 70px; font-weight: 400"
						type="button">
					<small v-if="!showPassword">
						{{ t('SHOW') }}
					</small>
					<small v-else>
						{{ t('HIDE') }}
					</small>
				</button>
			</div>

			<div class="line-height error-text" :class="{'shake' : shakeIt}" style="color: red">
				{{t(passwordError)}}
			</div>

			<div style="display: flex">
				<input :placeholder="t('PASSWORD (AGAIN)')" v-model="password2Input"
						:type="[showPassword2 ? 'text' : 'password']" style="flex-grow: 1" :id="`password2+${action}`"
						autocorrect="off" autocapitalize="none"/>
				<button v-on:click.prevent="showButton2()" class="button" style="width: 70px; font-weight: 400"
						type="button">
					<small v-if="!showPassword2">
						{{ t('SHOW') }}
					</small>
					<small v-else>
						{{ t('HIDE') }}
					</small>
				</button>
			</div>

			<div class="line-height error-text" :class="{'shake' : shakeIt}" style="color: red">
				{{t(password2Error)}}
			</div>
			
		</form>
		<button v-on:click.prevent="emailPassword()" class="button">
			{{ action === 'registerWithEmail' ? t('REGISTER') :
					action === 'addAnEmail' ? t('ADD EMAIL') : t('RESET PASSWORD')}}
		</button>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'emailPassword',
		components: {
		},
		data () {
			return {
				store: store,
				displayNameInput: '',
				emailInput: '',
				passwordInput: '',
				password2Input: '',
				showPassword: false,
				showPassword2: false,
				shakeIt: false,
				showError: true,
				passwordError: '',
				password2Error: '',
				emailError: '',
				displayNameError: '',
			}
		},
		props: {
			action: {},
		},
		async mounted () {
			if (this.action === 'registerWithEmail') {
				f.focusCursor(document, `displayName+${this.action}`)
			} else {
				f.focusCursor(document, `email+${this.action}`)
			}
			this.passwordHasErrors()
			this.password2HasErrors()
			this.emailHasErrors()
			if (this.action === 'registerWithEmail') {
				this.displayNameHasErrors()
			}
		},
		watch: {
			'passwordInput' () { this.passwordHasErrors(); this.password2HasErrors() },
			'password2Input' () { this.password2HasErrors() },
			'emailInput' () { this.emailHasErrors() },
			'displayNameInput' () { this.displayNameHasErrors() },
		},
		methods: {
			t (w) { return translations.t(w) },
			async emailPassword () {
				if (this.passwordError.length > 0 || this.password2Error.length > 0 || this.emailError.length > 0
						|| this.displayNameError.length > 0) {
					this.shakeFunction()
					return
				}
				this.showPassword = false
				this.showPassword2 = false
				let user = null
				if (this.action === 'registerWithEmail') {
					user = await api.registerWithEmail(this.emailInput, this.passwordInput, this.displayNameInput)
				} else if (this.action === 'addAnEmail') {
					user = await api.addAnEmail(this.emailInput, this.passwordInput)
				} else if (this.action === 'changePassword') {
					user = await api.changePassword(this.emailInput, this.passwordInput)
				}
				if (!user.error) {
					console.log('AND WHEN I GOT HERE WHAT WAS THE PAGE?', this.store.lastNonLoginRegisterPage)
					f.goToPage(this.store.lastNonLoginRegisterPage)
				} else if (user.error == 'Incorrect password for this email') {
					this.passwordError = user.error
					this.showError = true
					this.shakeFunction()
				} else if (user.error == "This email is already registered") {
					this.emailError = user.error
					this.showError = true
					this.shakeFunction()
				}
			},
			showButton () {
				f.focusCursor(document, `password+${this.action}`)
				this.showPassword = !this.showPassword
			},
			showButton2 () {
				f.focusCursor(document, `password2+${this.action}`)
				this.showPassword2 = !this.showPassword2
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
			password2HasErrors() {
				if (this.password2Input.length < 1 ) {
					this.password2Error = 'Required'
					return true
				} else if (this.passwordInput !== this.password2Input) {
					this.password2Error = 'Passwords don\'t match'
					return true
				} else {
					this.password2Error = ''
					return false
				}
			},
			emailHasErrors() {
				if (this.passwordError === 'Incorrect password for this email') {
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
			displayNameHasErrors() {
				if (this.displayNameInput.length < 1) {
					this.displayNameError = 'Required'
					return true
				} else if (f.hasIllegalSymbols(this.displayNameInput)) {
					this.displayNameError = 'Only these symbols are allowed: . _ - @'
					return true
				} else if (this.displayNameInput.length > 40) {
					this.displayNameError = 'Must be 40 characters or less'
					return true
				} else {
					this.displayNameError = ''
					return false
				}
			},
			shakeFunction () {
				this.shakeIt = true
				setTimeout(() => { this.shakeIt = false; }, 1000);
			},
		} // methods
	} // export
</script>
<style scoped>
	.button {
		width: 100%;
	}
</style>
