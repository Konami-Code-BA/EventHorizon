<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<password-input ref="passwordInput" :doublePassword="true" usage="ResetPassword" :enter="changePassword"
				style="width: 80%;"/>
		<button v-on:click.prevent="changePassword()" class="button">
			{{ t('CHANGE PASSWORD') }}
		</button>
		<flash-modal :text="t('PASSWORD CHANGED!')" ref="flashPasswordChangedForgot" :time="1000"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import passwordInput from '@/components/passwordInput.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import flashModal from '@/components/flashModal.vue'
	export default {
		name: 'resetPassword',
		components: {
			passwordInput,
			flashModal,
		},
		data () {
			return {
				store: store,
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async changePassword () {
				this.$refs.passwordInput.hasErrors()
				this.$refs.passwordInput.hasErrors2()
				if (
					this.$refs.passwordInput.error.length > 0
					|| this.$refs.passwordInput.error2.length > 0
				) {
					f.shakeFunction(this.$refs.passwordInput)
					return
				}
				this.$refs.passwordInput.showPassword = false
				this.$refs.passwordInput.showPassword2 = false
				this.store.loading = true

				let user = await api.changePassword(
					f.currentPage.args.email,
					this.$refs.passwordInput.password,
					f.currentPage.args.code,
					null,
				)
				if (!user.error) {
					this.store.loading = false
					await this.$refs.flashPasswordChangedForgot.flashModal()
					window.initMap()
					let nextPage = f.createNextPageFromCurrentPage()
					f.goToPage(nextPage)
					return
				}
				if (user.error == 'wrong code or password') {
					this.$refs.passwordInput1.error = 'Can\'t use this link'
				}
				this.store.loading = false
				f.shakeFunction(this.$refs.passwordInput)
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
