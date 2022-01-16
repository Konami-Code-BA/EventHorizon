<template>
	<div>
		<div class="footer" style="width: 100%">
			<tabs :num-tabs="4" :initial="0" :key="selectedTab" @on-click="(arg) => { selectTab(arg) }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1">
					<img src="@/assets/homeIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="2">
					<img src="@/assets/plusIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="3">
					<img v-if="isAuthenticatedUser" src="@/assets/profileIcon.png" class="icon"
							style="margin-bottom: 1px;"/>
					<img v-else src="@/assets/greyProfileIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="4">
					<img src="@/assets/shareIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
			</tabs>
		</div>
		<modal v-if="showShareModal" @closeModals="showShareModal = false">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end; padding-bottom: 5px;">
					<button v-on:click.prevent="showShareModal = false" class="no-border-button x-button">
						✖
					</button>
				</div>
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

				<div class="line-height"/>

				<div style="width: 100%">
					<button v-on:click.prevent="showShareModal = false; showImageModal = true" class="button" style="width: 100%">
						{{ t('SHARE IMAGE') }}
					</button>
				</div>
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
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'appFooter',
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
		components: {
			modal,
			tabs,
			qrCodeGenerator,
			urlDisplay,
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
	}
</style>