<template>
	<div>
		<div class="header" style="width: 100%;">
			<tabs :num-tabs="3" :initial="0" @on-click="(arg) => { selectedTab = arg }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1" style="vertical-align: bottom;">
					A/あ
				</div>
				<div slot="2">
					<button class="no-border-button" style="display: flex; flex-direction: row; align-items: center;"
							v-on:click.prevent="goToFront()">
						<div>EVENT</div>
						<div>
							<img src="@/assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div>HORIZON</div>
					</button>
				</div>
				<div slot="3">
					<img src="@/assets/threeBarsIcon.png" class="icon" style="height: 16px; margin-bottom: 3px;"/>
				</div>
			</tabs>
		</div>
		<modal v-if="selectedTab === 1" @closeModals="selectedTab = 0">
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
				<div class="line-height"></div>
				<div style="width: 100%">
					<button v-on:click.prevent="japanese()" class="button">
						日本語
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<modal v-if="selectedTab === 3" @closeModals="selectedTab = 0">
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
				<div class="line-height"></div>
				<div style="width: 100%">
					<button v-on:click.prevent="selectedTab = 0; $emit('modalPage', 'aboutUs', null)" class="button">
						ABOUT US
					</button>
				</div>
				<div class="line-height"></div>
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
		props: {
		},
		computed: {
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
		},
		watch: {
			'selectedTab' () {
				if (this.selectedTab != 0) {  // opens a modal
					f.setBackButtonToCloseModal(this, window, this.closeModal)
				} else if (this.selectedTab === 0 && !this.showQrModal) {  // closes a modal
					f.freeUpBackButton(this)
				} else if (this.selectedTab === 2) {
					this.goToFront()
				}
			},
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
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
			goToFront () {
				if (this.store.path !== 'front') {
					this.$emit('modalPage', 'front', null)
				}
			},
			goToLoginRegister () {
				this.$emit('modalPage', 'loginRegister', null)
				this.selectedTab = 0
			},
			async logout () {
				this.$emit('startLoading')
				await api.logout()
				location.reload()
			},
			closeModal () {
				f.freeUpBackButton(this)
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