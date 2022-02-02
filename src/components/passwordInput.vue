<template>
	<div>
		<div>
			<div style="display: flex; flex-direction: row">
				<input :placeholder="placeholder1" v-model="password"
					:type="[showPassword ? 'text' : 'password']" style="flex-grow: 1; width: 100%"
					:id="`password${usage}`" autocorrect="off" autocapitalize="none" v-on:keyup.enter="enter()"
					autocomplete="off"/>
				<button v-on:click.prevent="showButton()" class="button" style="width: 45px; font-size: 12px;"
						type="button">
					<small v-if="!showPassword">
						{{ t('SHOW') }}
					</small>
					<small v-else>
						{{ t('HIDE') }}
					</small>
				</button>
			</div>
			<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(error)}}</small>
			</div>
		</div>
		<div v-if="doublePassword">
			<div style="display: flex; flex-direction: row">
				<input :placeholder="placeholder2" v-model="password2"
					:type="[showPassword2 ? 'text' : 'password']" style="flex-grow: 1; width: 100%"
					:id="`password2${usage}`" autocorrect="off" autocapitalize="none" v-on:keyup.enter="enter()"
					autocomplete="off"/>
				<button v-on:click.prevent="showButton2()" class="button" style="width: 45px; font-size: 12px;"
						type="button">
					<small v-if="!showPassword2">
						{{ t('SHOW') }}
					</small>
					<small v-else>
						{{ t('HIDE') }}
					</small>
				</button>
			</div>
			<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
				<small>{{t(error2)}}</small>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'passwordInput',
		components: {
		},
		data () {
			return {
				password: '',
				showPassword: false,
				error: '',
				password2: '',
				showPassword2: false,
				error2: '',
				shakeIt: false,
				placeholder1: '',
				placeholder2: '',
			}
		},
		props: {
			doublePassword: { default: false },
			usage: {},
			customPlaceholder: { default: '' },
			enter: { type: Function, default: () => {} },
		},
		created () {
			if (this.customPlaceholder) {
				this.placeholder1 = this.t(this.customPlaceholder)
				this.placeholder2 = this.t(`CONFIRM ${this.customPlaceholder}`)
			} else {
				this.placeholder1 = this.t('PASSWORD')
				this.placeholder2 = this.t('CONFIRM PASSWORD')
			}
			
		},
		mounted () {
			this.hasErrors()
			this.hasErrors2()
		},
		watch: {
			'password' () { this.hasErrors(); this.hasErrors2() },
			'password2' () { this.hasErrors2() },
		},
		methods: {
			t (w) { return translations.t(w) },
			showButton () {
				f.focusCursor(document, `password${this.usage}`)
				this.showPassword = !this.showPassword
			},
			showButton2 () {
				f.focusCursor(document, `password2${this.usage}`)
				this.showPassword2 = !this.showPassword2
			},
			hasErrors() {
				if (this.password.length < 1 ) {
					this.error = 'Required'
					return true
				} else if (this.password.length < 4) {
					this.error = 'Must be 4 characters or more'
					return true
				} else if (this.password.length > 75) {
					this.error = 'Must be 75 characters or less'
					return true
				} else {
					this.error = ''
					return false
				}
			},
			hasErrors2() {
				if (this.password2.length < 1 ) {
					this.error2 = 'Required'
					return true
				} else if (this.password !== this.password2) {
					this.error2 = 'Passwords don\'t match'
					return true
				} else {
					this.error2 = ''
					return false
				}
			},
		}
	}
</script>
<style scoped>
</style>