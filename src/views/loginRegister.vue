<template>
	<div class="main" style="justify-content: center; overflow-y: scroll;">
		<div style="width: 80%">
			<div style="font-size: 24px; align-self: flex-start">{{ t('LOGIN WITH EMAIL') }}</div>
			<form v-on:keyup.enter="login()">
				<email-input ref="emailInput" usage="Login"/>
				<password-input ref="passwordInput" usage="Login"/>
			</form>
			<button v-on:click.prevent="login()" class="button">
				{{ t('LOGIN WITH EMAIL') }}
			</button>
			<br>
			<div style="width: 100%; display: flex; flex-direction: column; justify-content: center;">
				<button class="link-button" v-on:click.prevent="forgotPassword()">
					Forgot Password
				</button>
			</div>

			<div class="line-height"/>
			<div class="line-height"/>
			<div class="line-height"/>

			<button v-on:click.prevent="goToPage({ page: 'registerWithEmail', args: {} })" class="button">
				{{t('REGISTER EMAIL')}}
			</button>

			<div class="line-height"/>

			<line-button :pageToReturnTo="store.lastNonLoginRegisterPage" :wording="t('LINE LOGIN / REGISTER')"
					ref="lineButton"/>
		</div>
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import emailInput from '@/components/emailInput.vue'
	import passwordInput from '@/components/passwordInput.vue'
	import lineButton from '@/components/lineButton.vue'
	export default {
		name: 'loginRegister',
		components: {
			emailInput,
			passwordInput,
			lineButton,
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
			tryLine: { default: false },
		},
		async mounted () {
			if (this.$refs.lineButton && this.tryLine) {
				await this.$refs.lineButton.tryLineNewDevice()
			}
			f.focusCursor(document, 'emailLogin')
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToPage (pageDict) {
				f.goToPage(pageDict)
			},
			async login () {
				if (this.$refs.passwordInput.error.length > 0 || this.$refs.emailInput.error.length > 0) {
					f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput])
					return
				}
				this.$refs.passwordInput.showPassword = false
				this.store.loading = true
				let user = await api.login({
					'email': this.$refs.emailInput.email,
					'password': this.$refs.passwordInput.password
				})
				if (!user.error) {
					f.goToPage(this.store.lastNonLoginRegisterPage)
					window.initMap()
					this.store.loading = false
					return
				}
				if (user.error === 'This email is not registered') {
					this.$refs.emailInput.error = user.error
				}
				if (user.error === 'Incorrect password') {
					this.$refs.passwordInput.error = user.error
				}
				this.store.loading = false
				f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput])
			},
			forgotPassword () {
				f.goToPage({ page: 'forgotPassword', args: {} })
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
