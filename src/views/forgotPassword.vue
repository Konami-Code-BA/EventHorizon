<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<email-input ref="emailInput" usage="ForgotPassword" :enter="forgotPassword" style="width: 80%;"/>
		<button v-on:click.prevent="forgotPassword()" class="button">
			{{ t('SEND EMAIL') }}
		</button>
		<flash-modal :text="t('PASSWORD-CHANGE EMAIL SENT!')" ref="flashPasswordEmailSent" :time="2000"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import emailInput from '@/components/emailInput.vue'
	import flashModal from '@/components/flashModal.vue'
	export default {
		name: 'forgotPassword',
		components: {
			emailInput,
			flashModal,
		},
		data () {
			return {
				store: store,
			}
		},
		mounted () {
			f.focusCursor(document, 'emailForgotPassword')
		},
		methods: {
			t (w) { return translations.t(w) },
			async forgotPassword () {
				this.store.loading = true
				let returnUrl = f.createUrlForPasswordChange(this.$refs.emailInput.email)
				let user = await api.forgotPassword(this.$refs.emailInput.email, returnUrl)
				if (!user.error) {
					this.store.loading = false
					await this.$refs.flashPasswordEmailSent.flashModal()
				}
				if (user.error == "This email is not registered") {
					this.$refs.emailInput.error = user.error
				}
				this.store.loading = false
				
			}
		} // methods
	} // export
</script>
<style scoped>
	.button {
		width: 80%;
	}
</style>
