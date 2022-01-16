<template>
	<div>
		<div class="main">
			<div style="font-size: 36px;">{{ t('SETTINGS') }}</div>

			<div class="line-height"/>

			<div style="font-size: 24px;">{{ store.user.display_name }}</div>

			<div class="line-height"/>

			<button class="button" v-if="store.user.email === ''" v-on:click.prevent="openAddEmailModal()">
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
			<!--div>
				<h2>{{ t('CHANGE PASSWORD') }}</h2>
			</div-->
			<!--a href="https://lin.ee/UeSvNxR" class="line-coloring">
				<div class="line-button">
					<div class="line-alignment">
						<div>
							<img src="@/assets/line.png" class="line-img">
						</div>
						<div style="white-space: nowrap">
							ADD FRIEND
						</div>
					</div>
				</div>
			</a-->
		</div>
		<modal v-show="showAddEmailModal" @closeModals="closeAddEmailModal()">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="closeAddEmailModal()" class="no-border-button x-button">
						✖
					</button>
				</div>
				<form v-on:keyup.enter="addEmail()" style="width: 80%;">
					<email-input ref="emailInput" usage="AddEmail"/>
					<password-input ref="passwordInput" :doublePassword="true" usage="AddEmail"/>
				</form>
				<button v-on:click.prevent="addEmail()" class="button">
					{{ t('ADD EMAIL ADDRESS') }}
				</button>
			</div>
		</modal>
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
	export default {
		name: 'settings',
		components: {
			modal,
			lineButton,
			emailInput,
			passwordInput,
		},
		data () {
			return {
				store: store,
				showAddEmailModal: false,
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
			console.log('USER', this.store.user)
		},
		methods: {
			t (w) { return translations.t(w) },
			async updateUserDoGetEmails () {
				store.user.do_get_emails = !store.user.do_get_emails
				await api.updateUserDoGetEmails()
			},
			async updateUserDoGetLines () {
				store.user.do_get_lines = !store.user.do_get_lines
				await api.updateUserDoGetLines()
			},
			openAddEmailModal () {
				this.showAddEmailModal = true
			},
			closeAddEmailModal () {
				this.do_get_emails = this.store.user.do_get_emails
				this.showAddEmailModal = false
			},
			async addEmail () {
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
					this.closeAddEmailModal()
					this.store.loading = false
					return
				}
				if (user.error == 'Incorrect password for this email') {
					this.$refs.passwordInput.error = user.error
				}
				this.store.loading = false
				f.shakeFunction([this.$refs.passwordInput, this.$refs.emailInput])
			},
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
		transform: translate(110px, 0);
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
