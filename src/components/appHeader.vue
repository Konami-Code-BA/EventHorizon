<template>
	<div>
		<div class="header" style="width: 100%;">
			<tabs :num-tabs="5" :initial="0" @on-click="tab => { selectATab(tab) }"
					style="background-color: rgba(0, 0, 0, .5); height: 100%;">
				<div slot="1" style="width: 35px !important;">
					<img src="@/assets/backIcon.png" style="height: 22px; margin-top: 4px;"
							v-if="store.pages.length > 1">
					<div v-else style="width: 35px;"/>
				</div>
				<div slot="2" style="width: 35px !important;">
					<img src="@/assets/threeBarsIcon.png" style="height: 24px; margin-top: 4px;">
				</div>
				<div slot="3" style="width: 140px !important;">
					<div class="no-border-button" style="display: flex; flex-direction: row; align-items: center;">
						<div>EVENT</div>
						<div>
							<img src="@/assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div>HORIZON</div>
					</div>
				</div>
				<div slot="4" style="width: 0 !important; padding: 0 !important; margin: 0 !important;"/>
				<div slot="5" style="width: 70px !important;">
          			<div class="current-user" v-if="isAuthenticatedUser" style="color: #cae2ff; font-size: 10px;">
						{{ store.user.display_name }}
					</div>
          			<button class="no-border-button current-user" v-else v-on:click.prevent="goToLoginRegister()"
					  		style="font-size: 14px;">
						{{t('LOGIN')}}
					</button>
				</div>
			</tabs>
		</div>
		<modal v-if="showLanguageModal" @closeModals="showLanguageModal = false" ref="showLanguageModal"
				:key="showLanguageModal">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {$refs.showLanguageModal.closeModals()}" style="align-self: flex-end;"/>
				<div style="width: 100%;">
					<button v-on:click.prevent="$refs.showLanguageModal.closeModals(); english()" class="button">
						ENGLISH
					</button>
				</div>

				<div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="$refs.showLanguageModal.closeModals(); japanese()" class="button">
						日本語
					</button>
				</div>

				<div class="line-height"/>

			</div>
		</modal>
		<modal v-if="selectedTab === 2" @closeModals="selectedTab = 0" ref="selectedTab2">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {$refs.selectedTab2.closeModals()}" style="align-self: flex-end;"/>
				<div v-if="!isAuthenticatedUser" style="width: 100%">
					<button v-on:click.prevent="$refs.selectedTab2.closeModals(); goToLoginRegister();" class="button">
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
					<button v-on:click.prevent="$refs.selectedTab2.closeModals(); goToPage({ page: 'aboutUs', args: {} });"
							class="button">
						ABOUT US
					</button>
				</div>

				<div class="line-height" v-if="isAuthenticatedUser"/>

				<div style="width: 100%" v-if="isAuthenticatedUser">
					<button v-on:click.prevent="$refs.selectedTab2.closeModals(); showContactUs = true;"
							class="button">
						{{ t('CONTACT US') }}
					</button>
				</div>

				<div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="$refs.selectedTab2.closeModals(); goToPage({ page: 'faq', args: {} });"
							class="button">
						FAQ
					</button>
				</div>

				<div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="$refs.selectedTab2.closeModals(); showLanguageModal = true;"
							class="button">
						ENGLISH / 日本語
					</button>
				</div>

				<div class="line-height"/>

			</div>
		</modal>
		<modal v-if="showContactUs" @closeModals="showContactUs = false" ref="showContactUsModal" :key="showContactUs">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div style="width: 20px;"/>
					<div style="font-size: 20px; text-align: center;">
						{{ t('FEEDBACK') }}
					</div>
					<x-close-button :closeFunc="() => {$refs.showContactUsModal.closeModals()}"
							style="align-self: flex-end;"/>
				</div>
				<textarea :placeholder="t('FEEDBACK')" v-model="messageContent" type="text"
						autocapitalize="sentences" style="height: 90px;" autocomplete="off"/>
				<button v-on:click.prevent="feedback()" class="button">
					<div style="width: 100%; text-align: center;">{{ t('SEND') }}</div>
				</button>
			</div>
		</modal>
		<qr-code-generator v-if="showQrModal" @closeModals="showQrModal=false"/>
		<flash-modal :text="'SENT!'" ref="flashSent" :time="1500"/>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import tabs from '@/components/tabs.vue'
	import qrCodeGenerator from '@/components/qrCodeGenerator.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import xCloseButton from '@/components/xCloseButton.vue'
	import flashModal from '@/components/flashModal.vue'
	import f from '@/functions/functions.js'
	export default {
		name: 'appHeader',
		components: {
			modal,
			tabs,
			qrCodeGenerator,
			xCloseButton,
			flashModal,
		},
		data () {
			return {
				store: store,
				selectedTab: 0,
				showQrModal: false,
				showLanguageModal: false,
				showContactUs: false,
				messageContent: '',
			}
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
					window.location.replace(window.origin)
				} else if (tab === 1) {
					if (store.pages.length > 1) {
						f.goBack()
					}
				}
			},
			async english () {
				let lang = 'EN'
				store.user.language = lang
				await api.updateUserLanguage()
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
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
			async feedback () {
				this.store.loading = true
				await api.feedback(this.messageContent)
				this.messageContent = ''
				this.showContactUs = false
				this.store.loading = false
				await this.$refs.flashSent.flashModal()
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
		justify-content: space-around !important;
		width: 100%;
		max-width: 100%;
	}
	.button {
		width: 100%;
	}
	.current-user {
		width: 100%;
		max-width: 100%;
		height: 40px;
		max-height: 30px;
		overflow: hidden;
		vertical-align: middle;
		white-space: normal;
		overflow-wrap: normal;
  		word-break: normal;
		text-align: left;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: center;
		text-overflow: "...";
	}
</style>
