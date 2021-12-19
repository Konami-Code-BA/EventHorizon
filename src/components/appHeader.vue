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
							<img src="@/assets/eventhorizonTopIcon.png" style="height: 20px; vertical-align: middle;">
						</div>
						<div v-else>
							&nbsp;
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
				<div style="align-self: flex-end">
					<button v-on:click.prevent="selectedTab = 0" class="no-border-button">
						✖
					</button>
				</div>
				<div>
					<button v-on:click.prevent="english()" class="button">
						ENGLISH
					</button>
				</div>
				<div class="line-height"></div>
				<div>
					<button v-on:click.prevent="japanese()" class="button">
						日本語
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<modal v-if="selectedTab === 3" @closeModals="selectedTab = 0">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="selectedTab = 0" class="no-border-button">
						✖
					</button>
				</div>
				<div v-if="!isAuthenticatedUser">
					<button v-on:click.prevent="goToLoginRegister()" class="button">
						{{ t('LOGIN / REGISTER') }}
					</button>
				</div>
				<div v-else>
					<button v-on:click.prevent="logout()" class="button">
						{{ t('LOGOUT') }}
					</button>
				</div>
				<div class="line-height"></div>
				<div>
					<button v-on:click.prevent="selectedTab = 0; showQrModal = true" class="button">
						{{t('GET QR CODES')}}
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
	import apiFunctions from '@/functions/apiFunctions.js'
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
					this.goToEvents()
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
				await apiFunctions.updateUserLanguage()
			},
			async japanese () {
				let lang = 'JP'
				store.user.language = lang
				this.selectedTab = 0
				await apiFunctions.updateUserLanguage()
			},
			async goToEvents () {
				this.$emit('startLoading')
				if (this.$route.name !== 'events') {
					await this.$router.push({ name: 'events' })
					this.$emit('endLoading')
				} else {
					await location.reload()
				}
			},
			goToLoginRegister () {
				this.$emit('startLoading')
				if (this.$route.name !== 'loginRegister') {
					this.$router.push({ name: 'loginRegister' })
				}
				this.selectedTab = 0
				this.$emit('endLoading')
			},
			async logout () {
				this.$emit('startLoading')
				await apiFunctions.logout()
				this.selectedTab = 0
				this.goToEvents()
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
</style>