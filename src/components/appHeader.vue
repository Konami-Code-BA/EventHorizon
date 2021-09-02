<template>
	<div>
		<div class="header" style="width: 100%;">
			<tabs :num-tabs="3" :initial="0" @on-click="selectedTab = $event"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1" style="vertical-align: bottom;">
					A/文
				</div>
				<div slot="2">
					<div style="display: flex; flex-direction: row; align-items: center;">
						<div>EVENT</div>
						<div v-if="this.$route.name != 'front'">
							<img src="../assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div v-else>
							&nbsp;
						</div>
						<div>HORIZON</div>
					</div>
				</div>
				<div slot="3">
					<img src="../assets/threeBarsIcon.png" class="icon" style="height: 16px; margin-bottom: 3px;"/>
				</div>
			</tabs>
		</div>
		<transition name="fade">
			<modal v-show="selectedTab === 1" @closeModals="selectedTab = 0">
				<div slot="contents" class="language menu">
					<div style="align-self: flex-end">
						<button v-on:click.prevent="selectedTab = 0" class="no-border-button">
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
		<transition name="fade">
			<modal v-show="selectedTab === 3" @closeModals="selectedTab = 0">
				<div slot="contents" class="threeBars menu">
					<div style="align-self: flex-end">
						<button v-on:click.prevent="selectedTab = 0" class="no-border-button">
							✖
						</button>
					</div>
					<div>
						<button v-on:click.prevent="goToLoginRegister()" class="no-border-button"
								v-if="!isAuthenticatedUser">
							{{ t('LOGIN / REGISTER') }}
						</button>
					</div>
					<div>
						<button v-on:click.prevent="goToHome()" class="no-border-button"
								v-if="isAuthenticatedUser">
							{{ t('HOME') }}
						</button>
					</div>
					<div>
						<button v-on:click.prevent="goToSettings()" class="no-border-button"
								v-if="isAuthenticatedUser">
							{{ t('SETTINGS') }}
						</button>
					</div>
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
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import tabs from '@/components/tabs.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'appHeader',
		data () {
			return {
				store: store,
				selectedTab: 0,
			}
		},
		components: {
			modal,
			tabs,
		},
		props: {
		},
		computed: {
			isAuthenticatedUser () { return [1, 2].includes(store.user.groups[0]) },
		},
		watch: {
			'selectedTab' () {
				if (this.selectedTab === 2) {
					this.goToFront()
				}
			},
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
				this.selectedTab = 0
				await apiFunctions.updateUserLanguage()
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.selectedTab = 0
				await apiFunctions.updateUserLanguage()
			},
			goToHome () {
				if (this.$route.name !== 'guestHome') {
					this.$router.push({ name: 'guestHome' })
				}
				this.selectedTab = 0
			},
			goToFront () {
				if (this.$route.name !== 'front') {
					this.$router.push({ name: 'front' })
				}
				this.selectedTab = 0
			},
			goToLoginRegister () {
				if (this.$route.name !== 'loginRegister') {
					this.$router.push({ name: 'loginRegister' })
				}
				this.selectedTab = 0
			},
			goToSettings () {
				if (this.$route.name !== 'settings') {
					this.$router.push({ name: 'settings' })
				}
				this.selectedTab = 0
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
	.threeBars {
		right: 0;
	}
	.language {
		left: 0;
	}
	.languageIcon {
		height: 16px;
	}
</style>