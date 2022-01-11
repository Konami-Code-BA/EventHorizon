<template>
	<div>
		<div class="main">
			<div style="font-size: 36px;">{{ t('SETTINGS') }}</div>
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
			<button v-on:click.prevent="loginByLine()" class="button line-coloring" style="display: flex; flex-direction: row; align-items: center; justify-items: center;">
				<img src="@/assets/line.png" style="height: 27px;">
				<div>
					&nbsp;{{ t('ADD LINE') }}
				</div>
			</button>
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
				<register-with-email-internal :includeDisplayName="false" @closeModals="closeAddEmailModal()"/>
			</div>
		</modal>
	</div>
</template>
<script>
	import store from '@/store.js'
	import registerWithEmailInternal from '@/components/registerWithEmailInternal.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'settings',
		components: {
			modal,
			registerWithEmailInternal,
		},
		data () {
			return {
				store: store,
				showAddEmailModal: false,
				showAddEmailModal: false,
				stateCookie: JSON.parse('{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}')['state'],
			}
		},
		async mounted () {
			await this.tryLineNewDevice()
		},
		methods: {
			t (w) { return translations.t(w) },
			async updateUserDoGetEmails () {
				store.user.do_get_emails = !store.user.do_get_emails
				await api.updateUserDoGetEmails()  // update it in the DB
			},
			openAddEmailModal () {
				f.setBackButtonToCloseModal(this, window, this.closeAddEmailModal)
				this.showAddEmailModal = true
			},
			closeAddEmailModal () {
				f.freeUpBackButton(this)
				this.do_get_emails = this.store.user.do_get_emails
				this.showAddEmailModal = false
			},
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginByLine () {
				let loginChannelId = await api.secretsApi('login-channel-id')
				let state = await api.secretsApi('new-random-secret')
				document.cookie = `state=${state}; path=/`
				let lineLoginRedirectUrl = 'https%3A%2F%2Fwww.eventhorizon.vip%2Fsettings'
				if (process.env.PYTHON_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080%2Fsettings'
				} else if (process.env.PYTHON_ENV == '"test"') {
					lineLoginRedirectUrl = 'https%3A%2F%2Fevent-horizon-test.herokuapp.com%2Fsettings'
				}
				window.location.replace(`https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive&scope=profile%20openid`)
			},
			async tryLineNewDevice () {
				if (this.$route.query.code && this.stateCookie === this.$route.query.state) {
					await api.lineNewDevice(this.$route.query.code, '?page=loginRegister')
				}
			}
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
		transform: translate(60px, 0);
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
