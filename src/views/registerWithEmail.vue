<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<form v-on:keyup.enter="registerWithEmail()" style="width: 80%;">
			<display-name-input ref="displayNameInput" usage="Registration"/>
			<email-input ref="emailInput" usage="Registration"/>
			<password-input ref="passwordInput" :doublePassword="true" usage="Registration"/>
		</form>
		<button v-on:click.prevent="registerWithEmail()" class="button">
			{{ t('REGISTER') }}
		</button>
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
		} // methods
	} // export
</script>
<style scoped>
	.button {
		width: 80%;
	}
</style>
