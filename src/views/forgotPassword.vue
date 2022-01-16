<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<form v-on:keyup.enter="forgotPassword()" style="width: 80%;">
			<email-input ref="emailInput" usage="ForgotPassword"/>
		</form>
		<button v-on:click.prevent="forgotPassword()" class="button">
			{{ t('SEND CHANGE PASSWORD EMAIL') }}
		</button>
		<div v-if="showFlashModal" :class="flashModalClass" class="success-modal">
			{{ t('PASSWORD-CHANGE EMAIL SENT!') }}
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import emailInput from '@/components/emailInput.vue'
	export default {
		name: 'forgotPassword',
		components: {
			emailInput,
		},
		data () {
			return {
				store: store,
				showFlashModal: false,
				flashModalClass: null,
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
					await f.flashModal(this, 2000)  // flash email sent modal
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
	.success-modal {
		position: fixed;
		color: white;
		font-size: 24px;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		background-color: rgba(0, 0, 0, .8);
		z-index: 1000;
		width: 90%;
		text-align: center;
	}
</style>
