<template>
	<div>
		<div v-if="!loading">
			<div class="header">
				<div>
					<button v-on:click.prevent="mainMenu=!mainMenu" class="half-border-button"
						v-if="isAuthenticatedUser">
						<big>{{ t('MENU') }}</big>
					</button>
					<button v-on:click.prevent="$router.push({ name: 'loginRegister' })" class="half-border-button"
						v-else>
						<big>{{ t('LOGIN / REGISTER') }}</big>
					</button>
				</div>
				<div>
					<button v-on:click.prevent="languageMenu=!languageMenu" class="half-border-button">
							<big>A あ</big>
					</button>
				</div>
			</div>
			<div>
				<img src="../assets/eventhorizon.png" class="logo">
			</div>
			<transition name="fade">
				<modal class="mainMenu" v-show="mainMenu" @closeModals="languageMenu = false; mainMenu = false"
					id="mainMenu">
					<template v-slot:contents>
						<div style="text-align: right">
							<button v-on:click.prevent="mainMenu=!mainMenu" class="no-border-button">
								{{'✖\n'}}
							</button>
						</div>
						<div>
							<button v-on:click.prevent="$router.push({ name: 'home' })" class="half-border-button">
								<big>{{ t('HOME') }}</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="$router.push({ name: 'accountSettings' })"
								class="half-border-button">
								<big>{{ t('SETTINGS') }}</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="logout()" class="half-border-button">
								<big>{{ t('LOGOUT') }}</big>
							</button>
						</div><br>
					</template>
				</modal>
			</transition>
			<transition name="fade">
				<modal class="languageMenu" v-show="languageMenu" @closeModals="languageMenu = false; mainMenu = false"
					id="languageMenu">
					<template v-slot:contents>
						<div style="text-align: right">
							<button v-on:click.prevent="languageMenu=!languageMenu" class="no-border-button">
								✖
							</button>
						</div>
						<div>
							<button v-on:click.prevent="english()" class="half-border-button">
								<big>ENGLISH</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="japanese()" class="half-border-button">
								<big>日本語</big>
							</button>
						</div><br>
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
			isAuthenticatedUser () { return Boolean(store.user.display_name) },
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
				if (store.user.display_name) {
					await apiFunctions.updateUserLanguage()
				}
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.languageMenu = false
				if (store.user.display_name) {
					await apiFunctions.updateUserLanguage()
				}
			},
		}
	}
</script>
<style scoped>
	.mainMenu {
		position: absolute;
		padding: 20px;
		width: 50%;
		text-align: left;
		top: 30px;
		left: 0;
	}
	.languageMenu {
		position: absolute;
		padding: 20px;
		width: 50%;
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