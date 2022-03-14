<template>
	<div>
		<div>
			<input :placeholder="t('EMAIL')" v-model="email" type="text" :id="`email${usage}`" autocorrect="off"
					autocapitalize="none" style="width: 100%" v-on:keyup.enter="enter()" autocomplete="off"/>
		</div>
		<div class="line-height" :class="{'shake' : shakeIt}" style="color: red">
			<small>{{t(error)}}</small>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'emailInput',
		components: {
		},
		data () {
			return {
				email: '',
				error: '',
				shakeIt: false,
			}
		},
		props: {
			usage: {},
			enter: { type: Function, default: () => {} },
			dontStartError: { default: true },
		},
		mounted () {
			if(!this.dontStartError) {
				this.hasErrors()
			}
		},
		watch: {
			'email' () { this.hasErrors() },
		},
		methods: {
			t (w) { return translations.t(w) },
			hasErrors() {
				if (this.email.length < 1) {
					this.error = 'Required'
					return true
				} else if (this.hasInvalidEmailStructure(this.email) || f.hasIllegalSymbols(this.email)) {
					this.error = 'Required'
					return true
				} else if (this.email.length > 75) {
					this.error = 'Must be 75 characters or less'
					return true
				} else {
					this.error = ''
					return false
				}
			},
			hasInvalidEmailStructure(email) {
				let atSplit = email.split('@')
				if (atSplit.length != 2) {
					return true
				}
				let [mailPrefix, mailDomain] = atSplit
				let periodSplit = mailDomain.split('.')
				if (periodSplit.length != 2) {
					return true
				}
				let [domainPrefix, domainSuffix] = periodSplit
				if (mailPrefix.length < 1 || domainPrefix.length < 1 || domainSuffix.length < 2) {
					return true
				}
				return false
			},
		}
	}
</script>
<style scoped>
</style>