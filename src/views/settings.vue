<template>
	<div>
		<div class="main">
			<div>
				<h1>{{ t('SETTINGS') }}</h1>
			</div>
			<div class="dual-set">
				<div>
					<button class="no-border-button" v-on:click.prevent="do_get_emails=!do_get_emails">
						<div style="font-size: 18px;" v-if="store.user.email === ''">{{ t('ADD EMAIL ADDRESS') }}&nbsp;</div>
						<div style="font-size: 18px;" v-if="store.user.email !== ''">{{ t('GET EMAILS') }}&nbsp;</div>
					</button>
				</div>
				<div>
					<input type="checkbox" v-if="store.user.email !== ''" class="checkbox" v-model="do_get_emails"/>
				</div>
			</div>
			<div class="line-height"></div>
			<button v-on:click.prevent="loginByLine()" class="button line-coloring">
				<div class="line-button">
					<div class="line-alignment">
						<div>
							<img src="@/assets/line.png" class="line-img">
						</div>
						<div>
							ADD LINE
						</div>
					</div>
				</div>
			</button>
			<!--div>
				<h2>{{ t('CHANGE PASSWORD') }}</h2>
			</div-->
		</div>
		<modal v-show="showAddEmailModal" @closeModals="closeAddEmailModal()">
			<div slot="contents" class="addEmailModal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="closeAddEmailModal()" class="no-border-button">
						✖
					</button>
				</div>
				<register-with-email-internal
					@startLoading="$emit('startLoading')"
					@endLoading="$emit('endLoading')"
					:includeDisplayName="false"
				/>
			</div>
		</modal>
	</div>
</template>
<script>
	import store from '@/store.js'
	import appHeader from '@/components/appHeader.vue'
	import registerWithEmailInternal from '@/components/registerWithEmailInternal.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'settings',
		components: {
			appHeader,
			modal,
			registerWithEmailInternal,
		},
		data () {
			return {
				store: store,
				do_get_emails: store.user.do_get_emails,
				showAddEmailModal: false,
				stateCookie: JSON.parse('{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}')['state'],
			}
		},
		watch: {
			'do_get_emails' () {  // if do_get_emails changes
				if (this.do_get_emails) {  // if true, they want to get emails
					if (this.store.user.email !== '') {  // if user has an email set
						this.store.user.do_get_emails = true  // change the stored user's do_get_emails setting to true
					} else {  // if the user has no email set
						this.showAddEmailModal = true  // open up the AddEmailModal
						// if they save a new email, it will save a new stored user its do_get_emails
						// if they don't save a new email, it will not save a new stored user or its do_get_emails
					}
				} else {  // if false, they don't want to get emails
					this.store.user.do_get_emails = false  // change the stored user's do_get_emails setting to false
				}
			},
			async 'store.user.do_get_emails' () {  // if store.user.do_get_emails changes, update it in the DB
				await apiFunctions.updateUserDoGetEmails()  // update it in the DB
			},
		},
		async mounted () {
			await this.tryLineNewDevice()
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			closeAddEmailModal () {
				this.showAddEmailModal = false
				this.do_get_emails = this.store.user.do_get_emails
			},
			replaceAll (str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async loginByLine () {
				this.$emit('startLoading')
				let loginChannelId = await apiFunctions.secretsApiFunction('login_channel_id')
				let state = await apiFunctions.secretsApiFunction('new_random_secret')
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
					this.$emit('startLoading')
					await apiFunctions.lineNewDevice(this.$route.query.code, 'settings')
					this.$emit('endLoading')
					this.$router.push({ name: 'events' })
				}
			}
		} // methods
	} // export
</script>
<style scoped>
	.dual-set {
		height: 24px;
		display: flex;
		flex-direction: row;
		align-self: flex-start;
		align-items: flex-end;
		padding: 0;
	}
	.checkbox {
		height: 20px;
		width: 20px;
	}
	.addEmailModal {
		display: flex;
		flex-direction: column;
		align-items: center;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		max-height: 80%;
		width: 85%;
		max-width: 300px;
		z-index: 101;
		pointer-events: auto;
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
</style>
