<template>
	<div>
		<div class="header" style="width: 100%;">
			<tabs :num-tabs="3" :initial="0" @on-click="(arg) => { selectedTab = arg }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1" style="vertical-align: bottom;">
					A/文
				</div>
				<div slot="2">
					<button class="no-border-button" style="display: flex; flex-direction: row; align-items: center;"
							v-on:click.prevent="goToEvents()">
						<div>EVENT</div>
						<div v-if="this.$route.name != 'events'">
							<img src="../assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div v-else>
							&nbsp;
						</div>
						<div>HORIZON</div>
					</button>
				</div>
				<div slot="3">
					<img src="../assets/threeBarsIcon.png" class="icon" style="height: 16px; margin-bottom: 3px;"/>
				</div>
			</tabs>
		</div>
		<modal v-if="selectedTab === 1" @closeModals="selectedTab = 0">
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
		<modal v-if="selectedTab === 3" @closeModals="selectedTab = 0">
			<div slot="contents" class="threeBars menu">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="selectedTab = 0" class="no-border-button">
						✖
					</button>
				</div>
				<div v-if="!isAuthenticatedUser">
					<button v-on:click.prevent="goToLoginRegister()" class="no-border-button">
						{{ t('LOGIN / REGISTER') }}
					</button>
				</div>
				<div v-else>
					<button v-on:click.prevent="logout()" class="no-border-button">
						{{ t('LOGOUT') }}
					</button>
				</div>
				<div class="line-height"></div>
				<div>
					<button v-on:click.prevent="selectedTab = 0; showQrModal = true" class="no-border-button">
						{{t('GET QR CODES')}}
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<qr-code-generator v-if="showQrModal" @closeModal="showQrModal=false"/>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import tabs from '@/components/tabs.vue'
	import qrCodeGenerator from '@/components/qrCodeGenerator.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'appHeader',
		data () {
			return {
				store: store,
				selectedTab: 0,
				showQrModal: false,
			}
		},
		components: {
			modal,
			tabs,
			qrCodeGenerator,
		},
		props: {
		},
		computed: {
			isAuthenticatedUser () { return [1, 2].includes(store.user.groups[0]) },
		},
		watch: {
			'selectedTab' () {
				if (this.selectedTab === 2) {
					this.goToEvents()
				}
			},
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
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
			goToEvents () {
				if (this.$route.name !== 'events') {
					this.$router.push({ name: 'events' })
				} else {
					location.reload()
				}
				this.selectedTab = 0
			},
			goToLoginRegister () {
				if (this.$route.name !== 'loginRegister') {
					this.$router.push({ name: 'loginRegister' })
				}
				this.selectedTab = 0
			},
			async logout () {
				this.$emit('startLoading')
				await apiFunctions.logout()
				this.goToEvents()
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
		z-index: 100;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 80%;
		max-width: 300px;
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