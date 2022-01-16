<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<form v-on:keyup.enter="changePassword()" style="width: 80%;">
			<password-input ref="passwordInput" :doublePassword="true" usage="ResetPassword"/>
		</form>
		<button v-on:click.prevent="changePassword()" class="button">
			{{ t('CHANGE PASSWORD') }}
		</button>
		<div v-if="showFlashModal" :class="flashModalClass" class="success-modal">
			{{ t('PASSWORD CHANGED!') }}
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import passwordInput from '@/components/passwordInput.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'resetPassword',
		components: {
			passwordInput,
		},
		data () {
			return {
				store: store,
				showFlashModal: false,
				flashModalClass: null,
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async changePassword () {
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
				)
				if (!user.error) {
					this.store.loading = false
					await f.flashModal(this, 1000)  // flash password changed modal
					window.initMap()
					let nextPage = f.createNextPageFromCurrentPage()
					f.goToPage(nextPage)
					return
				}
				this.store.loading = false
				f.shakeFunction(this.$refs.passwordInput)
			},
		} // methods
	} // export
</script>
<style scoped>
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
