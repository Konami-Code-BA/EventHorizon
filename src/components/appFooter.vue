<template>
	<div>
		<div class="header-footer footer">
			<div>
				<img src="../assets/homeIcon.png" class="icon"/>
			</div>
			<div>
				<img src="../assets/homeIcon.png" class="icon"/>
			</div>
			<div>
				<img src="../assets/profileIcon.png" class="icon"/>
			</div>
			<div>
				<img src="../assets/gearIcon.png" class="icon"/>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'appFooter',
		data () {
			return {
				store: store,
				mainMenu: false,
				languageMenu: false,
			}
		},
		components: {
			modal,
		},
		props: {
		},
		computed: {
			isAuthenticatedUser () { return [1, 2].includes(store.user.groups[0]) },
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async logout () {
				this.$emit('startLoading')
				await apiFunctions.logout()
				if (this.$route.name !== 'front') {
					this.$router.push({ name: 'front' })
				} else {
					location.reload();
				}
			},
			async english () {
				let lang = 'EN'
				store.user.language = lang
				this.languageMenu = false
				await apiFunctions.updateUserLanguage()
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.languageMenu = false
				await apiFunctions.updateUserLanguage()
			},
			goToHome () {
				if (this.$route.name !== 'home') {
					this.$router.push({ name: 'home' })
				} else {
					this.mainMenu = false
				}
			},
			goToFront () {
				if (this.$route.name !== 'front') {
					this.$router.push({ name: 'front' })
				}
			},
			goToLoginRegister () {
				if (this.$route.name !== 'loginRegister') {
					this.$router.push({ name: 'loginRegister' })
				}
			},
			goToSettings () {
				if (this.$route.name !== 'settings') {
					this.$router.push({ name: 'settings' })
				} else {
					this.mainMenu = false
				}
			},
		}
	}
</script>
<style scoped>
</style>