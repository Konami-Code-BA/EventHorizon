<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<form v-on:keyup.enter="register()">
					<div>
						<input :placeholder="t('USERNAME')" v-model="usernameInput" type="text" class="box-item"
							id="username" autocorrect="off" autocapitalize="none"/>
					</div>
					<div class="box-item"></div>
					<div>
						<input :placeholder="t('EMAIL')" v-model="emailInput" type="email" class="box-item"
							autocorrect="off" autocapitalize="none"/>
					</div>
					<div class="box-item"></div>
					<div style="display: flex">
						<input :placeholder="t('PASSWORD')" v-model="passwordInput"
							:type="[showPassword ? 'text' : 'password']" class="box-item" style="flex-grow: 1"
							id="password" autocorrect="off" autocapitalize="none"/>
						<button v-on:click.prevent="showButton()" class="box-item" style="width: 60px"
							id="show" type="button">
							<small v-if="!showPassword">
								{{ t('SHOW') }}
							</small>
							<small v-else>
								{{ t('HIDE') }}
							</small>
						</button>
					</div>
					<div class="box-item"></div>
					<div style="display: flex">
						<input :placeholder="t('PASSWORD CONFIRMATION')" v-model="passwordInput2"
							:type="[showPassword2 ? 'text' : 'password']" class="box-item" style="flex-grow: 1"
							id="password2" autocorrect="off" autocapitalize="none" :class="{'shake' : shakeIt}"/>
						<button v-on:click.prevent="showButton2()" class="box-item" style="width: 60px"
							id="show" type="button">
							<small v-if="!showPassword2">
								{{ t('SHOW') }}
							</small>
							<small v-else>
								{{ t('HIDE') }}
							</small>
						</button>
					</div>
					<div v-if="showError" class="box-item" :class="{'shake' : shakeIt}" style="color: red">✘</div>
					<div v-else class="box-item">✅</div>
				</form>
				<button v-on:click.prevent="register()" class="box-item">
					{{ t('REGISTER') }}
				</button>
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="loading" v-else></div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import menusHeader from '@/components/menusHeader.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registerByEmail',
		components: {
			modal,
			menusHeader,
		},
		data () {
			return {
				store: store,
				loading: true,
				usernameInput: '',
				emailInput: '',
				passwordInput: '',
				passwordInput2: '',
				showPassword: false,
				showPassword2: false,
				shakeIt: false,
				showError: true,
			}
		},
		async mounted () {
			this.loading = false
			functions.focusCursor('username')
		},
		watch: {
			'passwordInput2' () {
				if (this.passwordInput === this.passwordInput2) {
					this.showError = false
				} else {
					this.showError = true
				}
			},
			'passwordInput' () {
				if (this.passwordInput === this.passwordInput2) {
					this.showError = false
				} else {
					this.showError = true
				}
			}
		},
		methods: {
			t (w) { return translations.t(w) },
			async register () {
				if (this.passwordInput !== this.passwordInput2) {
					this.shakeIt = true
					setTimeout(() => { this.shakeIt = false; }, 1000);
					return
				}
				this.showPassword = false
				this.showPassword2 = false
				await apiFunctions.register(this.usernameInput, this.emailInput, this.passwordInput)
				this.$router.push({ name: 'home' })
			},
			showButton () {
				functions.focusCursor('password')
				this.showPassword = !this.showPassword
			},
			showButton2 () {
				functions.focusCursor('password2')
				this.showPassword2 = !this.showPassword2
			},
		} // methods
	} // export
</script>
<style scoped>
	.shake {
		animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
		transform: translate3d(0, 0, 0);
	}
	@keyframes shake {
		10%, 90% {
		transform: translate3d(-1px, 0, 0);
		}
		20%, 80% {
		transform: translate3d(2px, 0, 0);
		}
		30%, 50%, 70% {
		transform: translate3d(-4px, 0, 0);
		}
		40%, 60% {
		transform: translate3d(4px, 0, 0);
		}
	}
</style>
