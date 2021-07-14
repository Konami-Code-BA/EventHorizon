<template>
	<div>
		<div>
			<div class="header">
				<div>
					<button v-on:click.prevent="mainMenu=true" class="no-border-button"
						v-if="isAuthenticatedUser">
						<big>{{ t('MENU') }}</big>
					</button>
					<button v-on:click.prevent="$router.push({ name: 'loginRegister' })" class="no-border-button"
						v-else>
						<big>{{ t('LOGIN / REGISTER') }}</big>
					</button>
				</div>
				<div>
					<button v-on:click.prevent="languageMenu=true" class="no-border-button">
							<big>A/文</big>
					</button>
				</div>
			</div>
			<div>
				<img src="../assets/eventhorizon.png" class="logo">
			</div>
			<transition name="fade">
				<modal v-show="mainMenu" @closeModals="languageMenu=false; mainMenu=false"
					id="mainMenu">
					<div slot="contents" class="mainMenu">
						<div style="text-align: right">
							<button v-on:click.prevent="mainMenu=false" class="no-border-button">
								{{'✖\n'}}
							</button>
						</div>
						<div>
							<button v-on:click.prevent="$emit('logoutLoading'); $router.push({ name: 'home' })" class="no-border-button">
								<big>{{ t('HOME') }}</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="$emit('logoutLoading'); $router.push({ name: 'accountSettings' })"
								class="no-border-button">
								<big>{{ t('SETTINGS') }}</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="logout()" class="no-border-button">
								<big>{{ t('LOGOUT') }}</big>
							</button>
						</div><br>
					</div>
				</modal>
			</transition>
			<transition name="fade">
				<modal v-show="languageMenu" @closeModals="languageMenu=false; mainMenu=false"
					id="languageMenu">
					<div slot="contents" class="languageMenu">
						<div style="align-self: flex-end">
							<button v-on:click.prevent="languageMenu=false" class="no-border-button">
								{{'✖\n'}}
							</button>
						</div>
						<div>
							<button v-on:click.prevent="english()" class="no-border-button">
								<big>ENGLISH</big>
							</button>
						</div><br><br>
						<div>
							<button v-on:click.prevent="japanese()" class="no-border-button">
								<big>日本語</big>
							</button>
						</div><br>
					</div>
				</modal>
			</transition>
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
		},
		computed: {
			isAuthenticatedUser () { return store.user.groups.includes(1) || store.user.groups.includes(2) },
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async logout () {
				this.$emit('logoutLoading')
				this.mainMenu = false
				await apiFunctions.logout()
				this.$router.push({ name: 'frontPage' })
				//location.reload()
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
		}
	}
</script>
<style scoped>
	.mainMenu {
		position: fixed;
		z-index: 10000;
		background-color: #00022e;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 40px;
		left: 0;
	}
	.languageMenu {
		display: flex;
		flex-direction: column;
		position: fixed;
		z-index: 10000;
		background-color: #00022e;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 40px;
		right: 0;
	}
	.languageIcon {
		height: 16px;
	}
</style>