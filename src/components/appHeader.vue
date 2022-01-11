<template>
	<div>
		<div class="header" style="width: 100%;">
			<tabs :num-tabs="5" :initial="0" @on-click="tab => { selectATab(tab) }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1">
					<img src="@/assets/backIcon.png" style="height: 22px; margin-top: 4px;">
				</div>
				<div slot="2">
					<img src="@/assets/languageIcon.png" style="height: 24px; margin-top: 4px;">
				</div>
				<div slot="3">
					<div class="no-border-button" style="display: flex; flex-direction: row; align-items: center;">
						<div>EVENT</div>
						<div>
							<img src="@/assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div>HORIZON</div>
					</div>
				</div>
				<div slot="4">
					<img src="@/assets/threeBarsIcon.png" class="icon" style="height: 21px; margin-bottom: 2px;"/>
				</div>
				<div slot="5"/>
			</tabs>
		</div>
		<modal v-if="selectedTab === 2" @closeModals="selectedTab = 0">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end; padding-bottom: 5px;">
					<button v-on:click.prevent="selectedTab = 0" class="no-border-button x-button">
						✖
					</button>
				</div>
				<div style="width: 100%">
					<button v-on:click.prevent="english()" class="button">
						ENGLISH
					</button>
				</div>
				<div class="line-height"/>
				<div style="width: 100%">
					<button v-on:click.prevent="japanese()" class="button">
						日本語
					</button>
				</div>
				<div class="line-height"/>
			</div>
		</modal>
		<modal v-if="selectedTab === 4" @closeModals="selectedTab = 0">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end; padding-bottom: 5px;">
					<button v-on:click.prevent="selectedTab = 0" class="no-border-button x-button">
						✖
					</button>
				</div>
				<div v-if="!isAuthenticatedUser" style="width: 100%">
					<button v-on:click.prevent="goToLoginRegister()" class="button">
						{{ t('LOGIN / REGISTER') }}
					</button>
				</div>
				<div v-else style="width: 100%">
					<button v-on:click.prevent="logout()" class="button">
						{{ t('LOGOUT') }}
					</button>
				</div>
				<div class="line-height"/>
				<div style="width: 100%">
					<button v-on:click.prevent="selectedTab = 0; goToPage({ page: 'aboutUs', args: {} })"
							class="button">
						ABOUT US
					</button>
				</div>
				<div class="line-height"/>
			</div>
		</modal>
		<qr-code-generator v-if="showQrModal" @closeModals="showQrModal=false"/>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import tabs from '@/components/tabs.vue'
	import qrCodeGenerator from '@/components/qrCodeGenerator.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
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
		computed: {
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
		},
		watch: {
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToPage (pageDict) {
				f.goToPage(pageDict)
			},
			selectATab (tab) {
				this.selectedTab = tab
				if (tab === 3) {
					location.reload()
				} else if (tab === 1) {
					f.goBack()
				}
			},
			async english () {
				let lang = 'EN'
				store.user.language = lang
				this.selectedTab = 0
				await api.updateUserLanguage()
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.selectedTab = 0
				await api.updateUserLanguage()
			},
			goToLoginRegister () {
				f.goToPage({ page: 'loginRegister', args: {} })
				this.selectedTab = 0
			},
			async logout () {
				this.store.loading = true
				f.goToPage({ page: 'home', args: {} })
				await api.logout()
				location.reload()
			},
			closeModal () {
				f.freeUpBackButton(this)  // this should change
				this.selectedTab = 0
				this.showQrModal = false
			},
		}
	}
</script>
<style scoped>
	.languageIcon {
		height: 16px;
	}
	.tabs {
		border-top: none !important;
		border-left: none !important;
		border-right: none !important;
	}
	.button {
		width: 100%;
	}
</style>