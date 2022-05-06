<template>
	<div class="main scroll-height" style="justify-content: center; overflow-y: scroll;">
		<div style="width: 80%" v-if="!showDone">
			<div style="font-size: 24px;">{{ t('LOGIN / REGISTER') }}</div>
			<form>
				<email-input ref="emailInput" usage="Login"
					:key="store.user.language+'emailInputLogin'"/>
				<button v-on:click.prevent="submit()" class="button">
					{{ t('SUBMIT') }}
				</button>
			</form>

			<div class="line-height"/>

			<div style="width: 100%; display: flex; flex-direction: column; justify-content: center;">
				<button class="link-button" v-on:click.prevent="openPrivacyPolicy()">
					{{t('Privacy Policy')}}
				</button>
			</div>

		</div>
		<div style="width: 80%" v-else>
			{{t('DONE! LOGIN EMAIL IS SENT!')}}
		</div>
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import emailInput from '@/components/emailInput.vue'
	export default {
		name: 'loginRegister',
		components: {
			emailInput,
		},
		data () {
			return {
				store: store,
				showDone: false,
			}
		},
		props: {
		},
		mounted () {
			f.focusCursor(document, 'emailLogin')
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToPage (pageDict) {
				f.goToPage(pageDict)
			},
			async submit () {
				this.$refs.emailInput.hasErrors()
				if (
					this.$refs.emailInput.error.length > 0
				) {
					f.shakeFunction(this.$refs.emailInput)
					return
				}
				this.store.loading = true
				let returnUrl = f.createUrlForLoginRegister(this.$refs.emailInput.email)
				let user = await api.startLoginRegister(this.$refs.emailInput.email, returnUrl)
				if (!user.error) {
					this.showDone = true
				}
				this.store.loading = false
			},
			openPrivacyPolicy () {
				window.open(
					'https://www.privacypolicytemplate.net/live.php?token=4ZdtebbIvgIe1fWqttdZ873Pal0uM2oh',
					'_blank'
				).focus()
			},
		} // methods
	} // export
</script>
<style scoped>
	.line-coloring {
		background-color: #00b300;
		color: white;
		padding: 0;
		border-color: #00b300;
	}
	.button {
		width: 100%;
	}
</style>
