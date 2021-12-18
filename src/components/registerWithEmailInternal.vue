<template>
	<div class="main" style="min-width: 300px;">
		<form v-on:keyup.enter="registerWithEmail()" :class="{'modal-style' : modalStyle}">
			<div v-if="includeDisplayName">
				<input :placeholder="t('DISPLAY NAME')" v-model="displayNameInput" type="text" id="displayName"
						autocorrect="off" autocapitalize="none" style="width: 100%"/>
				<div class="line-height error-text" :class="{'shake' : shakeIt}">
					{{t(displayNameError)}}
				</div>
			</div>
			<div>
				<input :placeholder="t('EMAIL')" v-model="emailInput" type="email" autocorrect="off"
						autocapitalize="none" id="email" style="width: 100%"/>
			</div>
			<div class="line-height error-text" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(emailError)}}</small>
			</div>
			<div style="display: flex">
				<input :placeholder="t('PASSWORD')" v-model="passwordInput" :type="[showPassword ? 'text' : 'password']"
						style="flex-grow: 1" id="password" autocorrect="off" autocapitalize="none"/>
				<button v-on:click.prevent="showButton()" class="button" style="width: 70px; font-weight: 400" id="show"
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
						:type="[showPassword2 ? 'text' : 'password']" style="flex-grow: 1" id="password2"
						autocorrect="off" autocapitalize="none"/>
				<button v-on:click.prevent="showButton2()" class="button" style="width: 70px; font-weight: 400"
						id="show" type="button">
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
		<button v-on:click.prevent="registerWithEmail()" class="button">
			{{ t('REGISTER') }}
		</button>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registerWithEmailInternal',
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
			includeDisplayName: { default: true },
			next: { default: null },
			modalStyle: { default: false },
		},
		async mounted () {
			if (this.includeDisplayName) {
				functions.focusCursor(document, 'displayName')
			} else {
				functions.focusCursor(document, 'email')
			}
			this.passwordHasErrors()
			this.password2HasErrors()
			this.emailHasErrors()
			if (this.includeDisplayName) {
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
			async registerWithEmail () {
				if (this.passwordError.length > 0 || this.password2Error.length > 0 || this.emailError.length > 0
						|| this.displayNameError.length > 0) {
					this.shakeFunction()
					return
				}
				this.showPassword = false
				this.showPassword2 = false
				this.$emit('startLoading')
				let error = null
				if (this.includeDisplayName) {
					error = await apiFunctions.registerWithEmail(this.emailInput, this.passwordInput,
							this.displayNameInput)
				} else {
					error = await apiFunctions.registerWithEmail(this.emailInput, this.passwordInput)
				}
				if (!error) {
					if (this.next) {
						this.$router.push({ name: this.next })
						this.$emit('endLoading')
						return
					} else {
						this.$emit('closeModals')
						this.$emit('endLoading')
						return
					}
				} else if (error == 'Incorrect password for this email') {
					this.passwordError = error
					this.showError = true
					this.shakeFunction()
				} else if (error == "This email is already registered") {
					this.emailError = error
					this.showError = true
					this.shakeFunction()
				}
			},
			showButton () {
				functions.focusCursor(document, 'password')
				this.showPassword = !this.showPassword
			},
			showButton2 () {
				functions.focusCursor(document, 'password2')
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
				if (this.passwordError
						=== 'Incorrect password for this email') {
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
			displayNameHasErrors() {
				if (this.displayNameInput.length < 1) {
					this.displayNameError = 'Required'
					return true
				} else if (this.hasIllegalSymbols(this.displayNameInput)) {
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
		} // methods
	} // export
</script>
<style scoped>
	.button {
		width: 80%;
	}
	.modal-style {
		width: 80%;
	}
</style>
