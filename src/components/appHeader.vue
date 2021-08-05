<template>
	<div>
		<div class="header-footer header">
			<div>
				<button v-on:click.prevent="languageMenu=true" class="no-border-button">
						A/文
				</button>
			</div>
			<div>
				<button v-on:click.prevent="goToFront()" class="no-border-button">
					<div>EVENT</div>
					<div v-if="this.$route.name != 'front'">
						<img src="../assets/eventhorizonTopIcon.png" class="line-height">
					</div>
					<div v-else>
						&nbsp;
					</div>
					<div>HORIZON</div>
				</button>
			</div>
			<div>
				<button v-on:click.prevent="mainMenu=true" class="no-border-button">
					<img src="../assets/threeBarsIcon.png" class="icon"/>
				</button>
			</div>
		</div>
		<transition name="fade">
			<modal v-show="mainMenu" @closeModals="languageMenu=false; mainMenu=false">
				<div slot="contents" class="main menu">
					<div style="align-self: flex-end">
						<button v-on:click.prevent="mainMenu=false" class="no-border-button">
							✖
						</button>
					</div>
					<div>
						<button v-on:click.prevent="goToLoginRegister()" class="no-border-button"
								v-if="!isAuthenticatedUser">
							{{ t('LOGIN / REGISTER') }}
						</button>
					</div>
					<div class="line-height"></div>
					<div>
						<button v-on:click.prevent="goToHome()" class="no-border-button"
								v-if="isAuthenticatedUser">
							{{ t('HOME') }}
						</button>
					</div>
					<div class="line-height"></div>
					<div>
						<button v-on:click.prevent="goToSettings()" class="no-border-button"
								v-if="isAuthenticatedUser">
							{{ t('SETTINGS') }}
						</button>
					</div>
					<div class="line-height"></div>
					<div>
						<button v-on:click.prevent="logout()" class="no-border-button"
								v-if="isAuthenticatedUser">
							{{ t('LOGOUT') }}
						</button>
					</div>
					<div class="line-height"></div>
				</div>
			</modal>
		</transition>
		<transition name="fade">
			<modal v-show="languageMenu" @closeModals="languageMenu=false; mainMenu=false">
				<div slot="contents" class="language menu">
					<div style="align-self: flex-end">
						<button v-on:click.prevent="languageMenu=false" class="no-border-button">
							✖
						</button>
					</div>
					<div>
						<button v-on:click.prevent="english()" class="no-border-button">
							ENGLISH
						</button>
					</div>
					<div class="line-height"></div>
					<div>
						<button v-on:click.prevent="japanese()" class="no-border-button">
							日本語
						</button>
					</div>
					<div class="line-height"></div>
				</div>
			</modal>
		</transition>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'appHeader',
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
				if (this.$route.name !== 'guestHome') {
					this.$router.push({ name: 'guestHome' })
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
	.menu {
		position: fixed;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		z-index: 10000;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 40px;
	}
	.main {
		right: 0;
	}
	.language {
		left: 0;
	}
	.languageIcon {
		height: 16px;
	}
</style>