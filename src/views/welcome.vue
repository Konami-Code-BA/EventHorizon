<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<form style="width: 80%;">
			<display-name-input ref="displayNameInput" usage="Registration"
					:key="store.user.language+'displayNameInputRegistration'"/>
			<button v-on:click.prevent="register()" class="button">
				{{ t('REGISTER') }}
			</button>
		</form>
	</div>
</template>
<script>
	import store from '@/store.js'
	import passwordInput from '@/components/passwordInput.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import flashModal from '@/components/flashModal.vue'
	import displayNameInput from '@/components/displayNameInput.vue'
	export default {
		name: 'welcome',
		components: {
			passwordInput,
			flashModal,
			displayNameInput,
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
		},
		computed: {
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
		},
		async mounted () {
			this.store.loading = true
			this.$emit('closeLanguage')
			this.email = f.currentPage.args.email
			this.code = f.currentPage.args.code
			f.removeArgFromUrl('email')
			f.removeArgFromUrl('code')
			await api.tryLogin(this.email, this.code)
			if (this.isAuthenticatedUser) {
				console.log('LOGGED IN')
				console.log('cookies', document.cookie)
				let nextPage = f.createNextPageFromCurrentPage()
				await f.getEvents()
				f.goToPage(nextPage)
			}
			this.store.loading = false
			f.focusCursor(document, 'displayNameRegistration')
		},
		methods: {
			t (w) { return translations.t(w) },
			async register () {
				console.log('REGISTER IS HAPPENING')
				this.$refs.displayNameInput.hasErrors()
				if (this.$refs.displayNameInput.error.length > 0) {
					f.shakeFunction([this.$refs.displayNameInput])
					return
				}
				this.store.loading = true
				await api.register(this.email, this.code,
						this.$refs.displayNameInput.displayName)
				if (this.isAuthenticatedUser) {
					console.log('REGISTERED')
					let nextPage = f.createNextPageFromCurrentPage()
					await f.getEvents()
					f.goToPage(nextPage)
				} else {
					this.$refs.displayNameInput.error = 'NOT AUTHENTICATED'
				}
				this.store.loading = false
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
