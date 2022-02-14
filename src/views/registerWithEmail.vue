<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center; overflow-y: scroll;">
		<form v-on:keyup.enter="registerWithEmail()" style="width: 80%;">
			<display-name-input ref="displayNameInput" usage="Registration"
					:key="store.user.language+'displayNameInputRegistration'"/>
			<email-input ref="emailInput" usage="Registration"
					:key="store.user.language+'emailInputRegistration'"/>
			<password-input ref="passwordInput" :doublePassword="true" usage="Registration"
					:key="store.user.language+'passwordInputRegistration'"/>
		</form>
		<button v-on:click.prevent="registerWithEmail()" class="button">
			{{ t('REGISTER') }}
		</button>

		<div class="line-height"/>

		<div style="width: 100%; display: flex; flex-direction: column; justify-content: center;">
			<button class="link-button" v-on:click.prevent="openPrivacyPolicy()">
				{{t('Privacy Policy')}}
			</button>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	import emailInput from '@/components/emailInput.vue'
	import passwordInput from '@/components/passwordInput.vue'
	import displayNameInput from '@/components/displayNameInput.vue'
	export default {
		name: 'registerWithEmail',
		components: {
			displayNameInput,
			emailInput,
			passwordInput,
		},
		data () {
			return {
				store: store,
			}
		},
		mounted () {
			f.focusCursor(document, 'displayNameRegistration')
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			async registerWithEmail () {
				this.$refs.passwordInput.hasErrors()
				this.$refs.passwordInput.hasErrors2()
				this.$refs.emailInput.hasErrors()
				this.$refs.displayNameInput.hasErrors()
				if (
					this.$refs.passwordInput.error.length > 0
					|| this.$refs.passwordInput.error2.length > 0
					|| this.$refs.emailInput.error.length > 0
					|| this.$refs.displayNameInput.error.length > 0
				) {
					f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput, this.$refs.displayNameInput])
					return
				}
				this.$refs.passwordInput.showPassword = false
				this.$refs.passwordInput.showPassword2 = false
				this.store.loading = true

				let user = await api.registerWithEmail(
					this.$refs.emailInput.email,
					this.$refs.passwordInput.password,
					this.$refs.displayNameInput.displayName
				)
				if (!user.error) {
					await f.getEvents()
					f.goToPage(this.store.lastNonLoginRegisterPage)
					window.initMap()
					this.store.loading = false
					return
				}
				if (user.error == "This email is already registered") {
					this.$refs.emailInput.error = user.error
				}
				this.store.loading = false
				f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput, this.$refs.displayNameInput])
			},
			openPrivacyPolicy () {
				window.open(
					'https://www.privacypolicytemplate.net/live.php?token=4ZdtebbIvgIe1fWqttdZ873Pal0uM2oh',
					'_blank'
				).focus()
			},
		} // methods
	} // export
</script>
<style scoped>
	.button {
		width: 80%;
	}
</style>
