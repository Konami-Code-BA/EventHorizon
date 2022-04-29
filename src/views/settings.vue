<template>
	<div class="main">
		<div class="main" style="overflow-y: hidden; width: 100%;">
			<div style="font-size: 36px;">{{ t('SETTINGS') }}</div>

			<div class="line-height"/>

			<div style="font-size: 24px;">{{ store.user.display_name }}</div>

  			<div class="line-height"/>

			<!-- Change display name input -->
			<div class="dual-set">
				<button v-on:click.prevent="showChangeDisplayNameModal = true" class="button" style="width: 100%">
					{{ t('EDIT DISPLAY NAME') }}&nbsp;
				</button>
			</div>

			<div class="line-height"/>

			<!-- E-mail preferences checkbox -->
			<div class="dual-set">
				<button class="button" style="width: 100%;"
						v-on:click.prevent="updateUserDoGetEmails()">
					{{ t('GET EMAILS') }}&nbsp;
				</button>
				<div class = "checkboxdiv">
					<input type="checkbox" class="checkbox" v-model="store.user.do_get_emails"
						:key="store.user.do_get_emails"/>
				</div>
			</div>

			<div class="line-height"/>

		</div>

		<!-- DISPLAY NAME CHANGE MODAL -->
		<modal v-if="showChangeDisplayNameModal" @closeModals="showChangeDisplayNameModal = false" ref="showChangeDisplayNameModal">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {$refs.showChangeDisplayNameModal.closeModals()}" style="align-self: flex-end;"/>
				<display-name-input ref="displayNameInput" :doublePassword="false" usage="Update"
						:enter="changeDisplayName" customPlaceholder="Enter Display Name" style="width: 100%;"/>
				<button v-on:click.prevent="changeDisplayName()" class="button" style="width: 100%">
					{{ t('EDIT DISPLAY NAME') }}
				</button>
        	</div>
		</modal>
    	<flash-modal :text="t('DONE!')" ref="flashDisplayNameChanged" :time="1000"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	import emailInput from '@/components/emailInput.vue'
	import passwordInput from '@/components/passwordInput.vue'
	import lineButton from '@/components/lineButton.vue'
	import modal from '@/components/modal.vue'
	import flashModal from '@/components/flashModal.vue'
	import displayNameInput from '@/components/displayNameInput.vue'
	import xCloseButton from '@/components/xCloseButton.vue'
	export default {
		name: 'settings',
		components: {
			modal,
			flashModal,
			displayNameInput,
			xCloseButton,
		},
		data () {
			return {
				store: store,
				showChangeDisplayNameModal: false,
			}
		},
		props: {
		},
		computed: {
			currentPage () {
				return f.currentPage
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async updateUserDoGetEmails () {
				store.user.do_get_emails = !store.user.do_get_emails
				await api.updateUserDoGetEmails()
			},
			async changeDisplayName() {
				this.$refs.displayNameInput.hasErrors()
				if (this.$refs.displayNameInput.error.length > 0) {
					f.shakeFunction([this.$refs.displayNameInput])
					return
				}
				store.user.display_name = this.$refs.displayNameInput.displayName
				await api.updateUserDisplayName()
				this.$refs.displayNameInput.DisplayName = ''
				this.showChangeDisplayNameModal = false
				await this.$refs.flashDisplayNameChanged.flashModal()
			}
		} // methods
	} // export
</script>
<style scoped>
	.dual-set {
		display: flex;
		flex-direction: row;
		align-self: stretch;
		align-items: center;
		vertical-align: stretch; 
		justify-content: center;
		padding: 0;
		margin: 0;
		width: 100%;
	}
	.checkbox {
		height: 20px;
		width: 20px;
		flex-shrink: 0;
	}
	.checkboxdiv {
		vertical-align: middle; 
		display: flex; 
		flex-direction: column; 
		justify-content: center; 
		position: fixed;
		height: 20px;
		width: 20px;
		transform: translate(96px, 0);
		z-index: 1;
	}
	.line-coloring {
		background-color: #00b300;
		color: white;
		padding: 0;
		border-color: #00b300;
	}
	.line-alignment {
		display: flex;
		flex-direction: row;
		align-items: center;
		width: 120px;
		justify-content: space-between;
		height: inherit !important;
	}
	.line-img {
		height: 27px;
		transform: translate(0, 2px);
	}
	.button {
		width: 100%;
		z-index:2;
	}
</style>
