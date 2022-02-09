<template>
	<div>
		<div class="footer" style="width: 100%">
			<tabs :num-tabs="4" :initial="0" :key="selectedTab" @on-click="(arg) => { selectTab(arg) }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1" class="tab">
					<img src="@/assets/homeIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="2" class="tab">
					<img src="@/assets/plusIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="3" class="tab">
					<img v-if="isAuthenticatedUser" src="@/assets/gearIcon.png" class="icon"
							style="margin-bottom: 1px;"/>
					<img v-else src="@/assets/greyGearIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="4" class="tab">
					<img src="@/assets/shareIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
			</tabs>
		</div>
		<modal v-if="showShareModal" @closeModals="showShareModal = false">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {showShareModal = false}" style="align-self: flex-end;"/>
				<div style="width: 100%">
					<button v-on:click.prevent="showShareModal = false; showQrModal = true" class="button" style="width: 100%">
						{{ t('SHARE QR CODE') }}
					</button>
				</div>

				<div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="showShareModal = false; showUrlModal = true" class="button" style="width: 100%">
						{{ t('SHARE URL') }}
					</button>
				</div>

				<!--div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="showShareModal = false; showImageModal = true" class="button" style="width: 100%">
						{{ t('SHARE IMAGE') }}
					</button>
				</div-->
			</div>
		</modal>
		<qr-code-generator v-if="showQrModal" @closeModals="showQrModal = false"/>
		<url-display v-if="showUrlModal" @closeModals="showUrlModal = false"/>
	</div>
</template>
<script>
	import store from '@/store'
	import modal from '@/components/modal'
	import tabs from '@/components/tabs.vue'
	import qrCodeGenerator from '@/components/qrCodeGenerator.vue'
	import urlDisplay from '@/components/urlDisplay.vue'
	import xCloseButton from '@/components/xCloseButton.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'appFooter',
		components: {
			modal,
			tabs,
			qrCodeGenerator,
			urlDisplay,
			xCloseButton,
		},
		data () {
			return {
				store: store,
				selectedTab: 0,
				showShareModal: false,
				showQrModal: false,
				showUrlModal: false,
				showImageModal: false,
				footerPages: ['home', 'addEvent', 'settings'],
				actions: [this.home, this.addEvent, this.settings, this.share],
			}
		},
		computed: {
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
		},
		mounted () {
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			selectTab (selectedTab) {
				this.actions[selectedTab-1]()
			},
			home () {
				this.$emit('homePage')
				f.goToPage({ page: 'home', args: {} })
			},
			addEvent () {
				f.goToPage({ page: 'addEvent', args: {} })
			},
			settings () {
				if(this.isAuthenticatedUser) {
					f.goToPage({ page: 'settings', args: {} })
				} else if (f.currentPage.page != 'loginRegister') {
					f.goToPage({ page: 'loginRegister', args: {} })
				}
			},
			share () {
				this.showShareModal = true
			},
		}
	}
</script>
<style scoped>
	.tabs {
		border-bottom: none !important;
		border-left: none !important;
		border-right: none !important;
		justify-content: space-around;
	}
	.tab {
		width: 70px !important;
	}
</style>