<template>
	<div>
		<div v-if="!loading">
			<div class="header">
				<div>
					<button v-on:click.prevent="mainMenu=!mainMenu" class="no-border-button"
						v-if="isAuthenticatedUser">
						<small>{{ t('MENU') }}</small>
					</button>
					<button v-on:click.prevent="$router.push({ name: 'login' })" class="no-border-button"
						v-else-if="!isLoginPage">
						<small>{{ t('LOGIN') }}</small>
					</button>
					<button v-on:click.prevent="$router.push({ name: 'registration' })" class="no-border-button"
						v-else>
						<small>{{ t('REGISTER') }}</small>
					</button>
				</div>
				<div>
					<button v-on:click.prevent="languageMenu=!languageMenu" class="no-border-button">
						<img src="../assets/languageIcon.png" class="languageIcon">
					</button>
				</div>
			</div>
			<div>
				<img src="../assets/eventhorizon.png" class="logo">
			</div>
			<transition name="fade">
				<modal class="mainMenu" v-show="mainMenu" @closeModals="closeAllModals" id="mainMenu">
					<template v-slot:contents>
						<div style="text-align: right">
							<button v-on:click.prevent="mainMenu=!mainMenu" class="close-button">
								<small>✖</small>
							</button>
						</div>
						<div>
							<button v-on:click.prevent="$router.push({ name: 'home' })" class="no-border-button">
								<small>{{ t('HOME') }}</small>
							</button>
						</div>
						<div>
							<button v-on:click.prevent="$router.push({ name: 'accountSettings' })" class="no-border-button">
								<small>{{ t('SETTINGS') }}</small>
							</button>
						</div>
						<div>
							<button v-on:click.prevent="logout()" class="no-border-button">
								<small>{{ t('LOGOUT') }}</small>
							</button>
						</div>
					</template>
				</modal>
			</transition>
			<transition name="fade">
				<modal class="languageMenu" v-show="languageMenu" @closeModals="closeAllModals" id="languageMenu">
					<template v-slot:contents>
						<div style="text-align: right">
							<button v-on:click.prevent="languageMenu=!languageMenu" class="close-button">
								<small>✖</small>
							</button>
						</div>
						<div>
							<button v-on:click.prevent="english()" class="no-border-button">
								<small>English</small>
							</button>
						</div>
						<div>
							<button v-on:click.prevent="japanese()" class="no-border-button">
								<small>日本語</small>
							</button>
						</div>
					</template>
				</modal>
			</transition>
		</div>
		<div class="box" v-else>
			Loading...
		</div>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'menusHeader',
		data () {
			return {
				store: store,
				mainMenu: false,
				languageMenu: false,
				loading: true,
				reload: false,
			}
		},
		components: {
			modal,
		},
		props: {
			isLoginPage: { default: false },
		},
		computed: {
			isAuthenticatedUser () { return Boolean(store.user.username) },
		},
		async mounted () {
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
			async logout () {
				this.mainMenu = false
				await apiFunctions.logout()
				this.$router.push({ name: 'frontPage' })
			},
			async english () {
				let lang = 'EN'
				store.user.language = lang
				this.languageMenu = false
				if (store.user.username) {
					await apiFunctions.updateUserLanguage()
				}
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.languageMenu = false
				if (store.user.username) {
					await apiFunctions.updateUserLanguage()
				}
			},
			closeAllModals () {
				this.languageMenu = false
				this.mainMenu = false
			},
		}
	}
</script>
<style scoped>
	.mainMenu {
		position: absolute;
		padding: 10px;
		width: 80px;
		text-align: left;
		top: 30px;
		left: 0;
	}
	.languageMenu {
		position: absolute;
		padding: 10px;
		width: 80px;
		text-align: left;
		top: 30px;
		right: 0;
	}
	.languageIcon {
		height: 16px;
	}
	.fade-enter-active, .fade-leave-active {
		transition: opacity .3s;
	}
</style>