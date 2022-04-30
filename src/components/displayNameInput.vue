<template>
	<div>
		<div>
			<input :placeholder="placeholder" v-model="displayName" type="text" :id="`displayName${usage}`"
					autocorrect="off" autocapitalize="words" style="width: 100%" v-on:keyup.enter="enter()"
					autocomplete="off"/>
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
		name: 'displayNameInput',
		components: {
		},
		data () {
			return {
				displayName: '',
				error: '',
				shakeIt: false,
				placeholder: '',
			}
		},
		props: {
			usage: {},
			dontStartError: { default: true },
			enter: { type: Function, default: () => {} },
		},
		mounted () {
			if (!this.dontStartError) {
				this.hasErrors()
			}
			if (this.usage === 'PlusOne') {
				this.placeholder = this.t('+1 NAME')
			} else {
				this.placeholder = this.t('DISPLAY NAME')
			}
		},
		watch: {
			'displayName' () { this.hasErrors() },
		},
		methods: {
			t (w) { return translations.t(w) },
			hasErrors() {
				if (this.displayName.length < 1) {
					this.error = 'Required'
					return true
				} else if (f.hasIllegalSymbols(this.displayName)) {
					this.error = 'Only these symbols are allowed: . _ - @'
					return true
				} else if (this.displayName.length > 40) {
					this.error = 'Must be 40 characters or less'
					return true
				} else {
					this.error = ''
					return false
				}
			},
		}
	}
</script>
<style scoped>
</style>