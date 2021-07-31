<template>
	<div>
		<div class="box">
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
			<!--div>
				<h2>{{ t('CHANGE PASSWORD') }}</h2>
			</div-->
		</div>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		<transition name="fade">
			<modal v-show="showAddEmailModal" @closeModals="closeAddEmailModal()">
				<div slot="contents" class="addEmailModal">
					<div style="text-align: right">
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
		</transition>
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
			}
		},
		watch: {
			'do_get_emails' () {  // if do_get_emails changes
				if (this.do_get_emails) {  // if true, they want to get emails
					if (store.user.email !== '') {  // if user has an email set
						store.user.do_get_emails = true  // change the stored user's do_get_emails setting to true
					} else {  // if the user has no email set
						this.showAddEmailModal = true  // open up the AddEmailModal
						// if they save a new email, it will save a new stored user its do_get_emails
						// if they don't save a new email, it will not save a new stored user or its do_get_emails
					}
				} else {  // if false, they don't want to get emails
					store.user.do_get_emails = false  // change the stored user's do_get_emails setting to false
				}
			},
			async 'store.user.do_get_emails' () {  // if store.user.do_get_emails changes, update it in the DB
				await apiFunctions.updateUserDoGetEmails()  // update it in the DB
			},
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			closeAddEmailModal () {
				this.showAddEmailModal = false
				this.do_get_emails = store.user.do_get_emails
			}
		} // methods
	} // export
</script>
<style scoped>
	.dual-set {
		height: 24px;
		display: flex;
		flex-direction: row;
		align-items: flex-end;
		padding: 0;
	}
	.checkbox {
		height: 20px;
		width: 20px;
	}
	.addEmailModal {
		position: fixed;
		z-index: 10000;
		background-color: #18002e;
		border-radius: 15px;
		border: 1px solid #5300e1;
		padding: 20px;
		width: 85%;
		height: 100%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, 0);
	}
</style>
