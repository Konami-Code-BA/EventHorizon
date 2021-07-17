<template>
	<div>
		<form v-on:keyup.enter="registerWithEmail()">
			<div v-if="includeDisplayName">
				<input :placeholder="t('DISPLAY NAME')" v-model="displayName" type="text" class="box-item"
					id="displayName" autocorrect="off" autocapitalize="none"/>
			</div>
			<div class="box-height"></div>
			<div>
				<input :placeholder="t('EMAIL')" v-model="emailInput" type="email" class="box-item"
					autocorrect="off" autocapitalize="none" id="email"/>
			</div>
			<div class="box-height" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{emailError}}</small>
			</div>
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
			<div class="box-height"></div>
			<div style="display: flex">
				<input :placeholder="t('PASSWORD (AGAIN)')" v-model="passwordInput2"
					:type="[showPassword2 ? 'text' : 'password']" class="box-item" style="flex-grow: 1"
					id="password2" autocorrect="off" autocapitalize="none"/>
				<button v-on:click.prevent="showButton2()" class="box-item" style="width: 70px"
					id="show" type="button">
					<small v-if="!showPassword2">
						{{ t('SHOW') }}
					</small>
					<small v-else>
						{{ t('HIDE') }}
					</small>
				</button>
			</div>
			<div v-if="showError" class="box-height" :class="{'shake' : shakeIt}" style="color: red">
				✘&nbsp;<small>{{passwordError}}</small>
			</div>
			<div v-else class="box-height">✅</div>
		</form>
		<button v-on:click.prevent="registerWithEmail()" class="box-item">
			{{ t('REGISTER') }}
		</button>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registerWithEmailInternal',
		components: {
		},
		data () {
			return {
				store: store,
				loading: true,
				displayName: '',
				emailInput: '',
				passwordInput: '',
				passwordInput2: '',
				showPassword: false,
				showPassword2: false,
				shakeIt: false,
				showError: true,
				passwordError: '',
				emailError: '',
			}
		},
		props: {
			includeDisplayName: { default: true }
		},
		async mounted () {
			if (this.includeDisplayName) {
				functions.focusCursor('displayName')
			} else {
				functions.focusCursor('email')
			}
		},
		watch: {
			'passwordInput2' () { this.checkInputs() },
			'passwordInput' () { this.checkInputs() },
			'emailInput' () { this.checkInputs() },
			'displayName' () { this.checkInputs() },
		},
		methods: {
			t (w) { return translations.t(w) },
			async registerWithEmail () {
				if (this.checkInputs()) {
					this.shakeFunction()
					return
				}
				this.showPassword = false
				this.showPassword2 = false
				//this.$emit('closeModal')
				this.$emit('startLoading')
				let error = null
				if (this.includeDisplayName) {
					error = await apiFunctions.registerWithEmail(this.emailInput, this.passwordInput, this.displayName)
				} else {
					error = await apiFunctions.registerWithEmail(this.emailInput, this.passwordInput)
				}
				if (!error) {
					this.$router.push({ name: 'home' })
					this.$emit('endLoading')
				} else if (error == "this email is already registered and this isn't the correct password for it") {
					this.$emit('endLoading')
					this.passwordError = error
					this.showError = true
					this.shakeFunction()
				} else if (error == "this email is already registered") {
					this.$emit('endLoading')
					this.emailError = error
					this.showError = true
					this.shakeFunction()
				}
				this.$emit('endLoading')
			},
			showButton () {
				functions.focusCursor('password')
				this.showPassword = !this.showPassword
			},
			showButton2 () {
				functions.focusCursor('password2')
				this.showPassword2 = !this.showPassword2
			},
			checkInputs () {
				if (this.passwordInput !== this.passwordInput2 || this.passwordInput === '' ||
						this.passwordInput2 === '' || this.emailInput === '' || !this.emailInput.includes('@') ||
						!this.emailInput.includes('.') || (this.includeDisplayName && this.displayName === '')) {
					this.showError = true
					return true
				} else {
					this.showError = false
					return false
				}
			},
			shakeFunction () {
				this.shakeIt = true
				setTimeout(() => { this.shakeIt = false; }, 1000);
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
