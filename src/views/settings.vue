<template>
	<div>
		<div class="main" style="overflow-y: scroll;">
			<div style="font-size: 36px;">{{ t('SETTINGS') }}</div>

			<div class="line-height"/>

			<div style="font-size: 24px;">{{ store.user.display_name }}</div>

  	<div class="line-height"/>
<!-- Change display name input -->
      <div class="dual-set">
				<button v-on:click.prevent="updateUserDisplayName()" class="button" style="width: 100%">
					{{ 'EDIT DISPLAY NAME' }}&nbsp;
				</button>
			</div>
			<div class="line-height"/>
      <!-- E-mail preferences checkbox -->
			<button class="button" v-if="store.user.email === ''" v-on:click.prevent="showAddEmailModal = true">
				{{ t('ADD EMAIL ADDRESS') }}
			</button>
			<div v-else class="dual-set">
				<button class="button" style="width: 100%"
						v-on:click.prevent="updateUserDoGetEmails()">
					{{ t('GET EMAILS') }}&nbsp;
				</button>
				<input type="checkbox" class="checkbox" v-model="store.user.do_get_emails"
						:key="store.user.do_get_emails"/>
			</div>

			<div class="line-height"/>

			<line-button :pageToReturnTo="currentPage" :wording="t('ADD LINE')" v-if="store.user.line_id === ''"
					ref="lineButton"/>
			<div v-else class="dual-set">
				<button class="button" style="width: 100%"
						v-on:click.prevent="updateUserDoGetLines()">
					{{ t('GET LINE MESSAGES') }}&nbsp;
				</button>
				<input type="checkbox" class="checkbox" v-model="store.user.do_get_lines"
						:key="store.user.do_get_lines"/>
			</div>

			<div class="line-height"/>

			<button class="button" v-if="store.user.password != ''" v-on:click.prevent="showChangePasswordModal = true">
				{{ t('CHANGE PASSWORD') }}
			</button>
		</div>

		<modal v-show="showAddEmailModal" @closeModals="showAddEmailModal = false">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="showAddEmailModal = false" class="no-border-button x-button">
						✖
					</button>
				</div>
				<form v-on:keyup.enter="addEmail()" style="width: 80%;">
					<email-input ref="emailInput" usage="AddEmail"
							:key="store.user.language+'emailInputAddEmail'"/>
					<password-input ref="passwordInput" :doublePassword="true" usage="AddEmail"
							:key="store.user.language+'passwordInputAddEmail'"/>
				</form>
				<button v-on:click.prevent="addEmail()" class="button">
					{{ t('ADD EMAIL ADDRESS') }}
				</button>
			</div>
		</modal>
		<modal v-show="showChangePasswordModal" @closeModals="showChangePasswordModal = false">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="showChangePasswordModal = false" class="no-border-button x-button">
						✖
					</button>
				</div>
				<form v-on:keyup.enter="changePassword()" style="width: 100%;">
					<password-input ref="passwordInput1" :doublePassword="false" usage="ChangePassword1"
							customPlaceholder="CURRENT PASSWORD"/>
					<password-input ref="passwordInput2" :doublePassword="true" usage="ChangePassword2"
							customPlaceholder="NEW PASSWORD"/>
				</form>
				<button v-on:click.prevent="changePassword()" class="button" style="width: 100%">
					{{ t('CHANGE PASSWORD') }}
				</button>
<!-- DISPLAY NAME CHANGE MODAL -->
        	<!-- <modal v-show="showChangeDisplayNameModal" @closeModals="showChangeDisplayNameModal = false">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="showChangeDisplayNameModal = false" class="no-border-button x-button">
						✖
					</button>
				</div>
				<form v-on:keyup.enter="changePassword()" style="width: 100%;">
					<password-input ref="passwordInput1" :doublePassword="false" usage="ChangePassword1"
							customPlaceholder="CURRENT PASSWORD"/>
					<password-input ref="passwordInput2" :doublePassword="true" usage="ChangePassword2"
							customPlaceholder="NEW PASSWORD"/>
				</form>
				<button v-on:click.prevent="changePassword()" class="button" style="width: 100%">
					{{ t('CHANGE PASSWORD') }}
				</button> -->

			</div>
		</modal>
		<flash-modal :text="t('PASSWORD CHANGED!')" ref="flashPasswordChangedSettings" :time="1000"/>
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
	export default {
		name: 'settings',
		components: {
			modal,
			lineButton,
			emailInput,
			passwordInput,
			flashModal,
		},
		data () {
			return {
				store: store,
				showAddEmailModal: false,
				showChangePasswordModal: false,
        // showChangeDisplayNameModal = false
			}
		},
		props: {
			tryLine: { default: false },
		},
		computed: {
			currentPage () {
				return f.currentPage
			}
		},
		async mounted () {
			if (this.$refs.lineButton && this.tryLine) {
				await this.$refs.lineButton.tryLineNewDevice()
			}
			f.focusCursor(document, 'emailAddEmail')
		},
		methods: {
			t (w) { return translations.t(w) },
			async updateUserDoGetEmails () {
				store.user.do_get_emails = !store.user.do_get_emails
				await api.updateUserDoGetEmails()
			},
      async updateUserDisplayName() {
				store.user.display_name = "Successfully changed!"
				await api.updateUserDisplayName()
			},
			async updateUserDoGetLines () {
				store.user.do_get_lines = !store.user.do_get_lines
				await api.updateUserDoGetLines()
			},
			async addEmail () {
				this.$refs.passwordInput.hasErrors()
				this.$refs.passwordInput.hasErrors2()
				this.$refs.emailInput.hasErrors()
				if (
					this.$refs.passwordInput.error.length > 0
					|| this.$refs.passwordInput.error2.length > 0
					|| this.$refs.emailInput.error.length > 0
				) {
					f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput])
					return
				}
				this.$refs.passwordInput.showPassword = false
				this.$refs.passwordInput.showPassword2 = false
				this.store.loading = true

				let user = await api.addAnEmail(
					this.$refs.emailInput.email,
					this.$refs.passwordInput.password,
				)
				if (!user.error) {
					f.goToPage(this.store.lastNonLoginRegisterPage)
					window.initMap()
					this.showAddEmailModal = false
					this.store.loading = false
					return
				}
				if (user.error == 'Incorrect password for this email') {
					this.$refs.passwordInput.error = user.error
				}
				this.store.loading = false
				f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput])
			},
			async changePassword () {
				this.$refs.passwordInput.hasErrors()
				this.$refs.passwordInput.hasErrors2()
				this.$refs.passwordInput2.hasErrors()
				if (
					this.$refs.passwordInput1.error.length > 0
					|| this.$refs.passwordInput2.error2.length > 0
				) {
					f.shakeFunction([this.$refs.passwordInput1, this.$refs.passwordInput2])
					return
				}
				this.$refs.passwordInput1.showPassword = false
				this.$refs.passwordInput2.showPassword = false
				this.$refs.passwordInput2.showPassword2 = false
				this.store.loading = true

				let user = await api.changePassword(
					this.store.user.email,
					this.$refs.passwordInput2.password,
					null,
					this.$refs.passwordInput1.password,
				)
				if (!user.error) {
					this.showChangePasswordModal = false
					this.$refs.passwordInput1.password = ''
					this.$refs.passwordInput2.password = ''
					this.$refs.passwordInput2.password2 = ''
					this.store.loading = false
					await this.$refs.flashPasswordChangedSettings.flashModal()
					return
				}
				if (user.error == 'wrong code or password') {
					this.$refs.passwordInput1.error = 'CURRENT PASSWORD IS INCORRECT'
				}
				this.store.loading = false
				f.shakeFunction([this.$refs.passwordInput1, this.$refs.passwordInput2])
			},

      // Display name change
      // async changeDisplayName() {
			// 	let user = await api.changePassword(
			// 		this.store.user.email,
			// 		this.$refs.passwordInput2.password,
			// 		null,
			// 		this.$refs.passwordInput1.password,
			// 	)
			// 		this.showChangePasswordModal = false
			// 		this.$refs.passwordInput1.password = ''
			// 		this.$refs.passwordInput2.password = ''
			// 		this.$refs.passwordInput2.password2 = ''
			// 		this.store.loading = false
			// 		await this.$refs.flashPasswordChangedSettings.flashModal()
      // }
		} // methods
	} // export
</script>
<style scoped>
	.dual-set {
		display: flex;
		flex-direction: row;
		align-self: center;
		align-items: center;
		justify-content: center;
		padding: 0;
		width: 80%;
	}
	.checkbox {
		position: fixed;
		height: 20px;
		width: 20px;
		transform: translate(90px, 0);
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
		width: 80%;
		z-index:2;
	}
</style>
