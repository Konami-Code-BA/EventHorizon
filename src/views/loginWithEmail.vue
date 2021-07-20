<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<form v-on:keyup.enter="login()">
					<div>
						<input :placeholder="t('EMAIL')" v-model="emailInput" type="text" class="box-item"
							id="email" autocorrect="off" autocapitalize="none"/>
					</div>
					<div class="box-height"><small>{{emailError}}</small></div>
					<div style="display: flex">
						<input :placeholder="t('PASSWORD')" v-model="passwordInput"
							:type="[showPassword ? 'text' : 'password']" class="box-item" style="flex-grow: 1"
							id="password" autocorrect="off" autocapitalize="none"/>
						<button v-on:click.prevent="showButton()" class="box-item" style="width: 70px"
							id="show" type="button">
							<small v-if="!showPassword">
								{{ t('SHOW') }}
							</small>
							<small v-else>
								{{ t('HIDE') }}
							</small>
						</button>
					</div>
				</form>
				<div class="box-height"><small>{{passwordError}}</small></div>
				<button v-on:click.prevent="login()" class="box-item">
					{{ t('LOGIN') }}
				</button>
				<!--button class="no-border-button small-button" v-on:click.prevent="sendEmail()">
					<small><small>{{t('FORGOT PASSWORD')}}</small></small>
				</button-->
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="loading" v-else></div>
	</div>
</template>
<script src="https://smtpjs.com/v3/smtp.js"></script>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'loginWithEmail',
		components: {
			menusHeader,
			modal,
		},
		data () {
			return {
				store: store,
				loading: true,
				emailInput: '',
				passwordInput: '',
				showPassword: false,
				emailError: '',
				passwordError: '',
			}
		},
		async mounted () {
			this.loading = false
			functions.focusCursor('email')
		},
		methods: {
			t (w) { return translations.t(w) },
			async login () {
				if (!this.inputsHaveErrors()) {
					this.showPassword = false
					this.loading = true
					let error = await apiFunctions.login({'email': this.emailInput, 'password': this.passwordInput})
					this.loading = false
					if (!error) {
						this.$router.push({ name: 'home' })
					} else if (error === 'this email is not registered') {
						this.emailError = error
					} else if (error === 'incorrect password') {
						this.passwordError = error
					}
				}
			},
			showButton () {
				functions.focusCursor('password')
				this.showPassword = !this.showPassword
			},
			async sendEmail() {
				await apiFunctions.sendEmail()
			},
			inputsHaveErrors () {
				if (this.passwordInput === '' || this.emailInput === '' || !this.emailInput.includes('@') ||
						!this.emailInput.includes('.')) {
					//this.showError = true
					return true
				} else {
					//this.showError = false
					return false
				}
			},
			//goToPage2 () {
			//	this.$router.push({ name: 'pageTwo', params: { thruParams: 'this was sent from the login page' } })
			//},
		} // methods
	} // export
</script>
<style scoped>
</style>
