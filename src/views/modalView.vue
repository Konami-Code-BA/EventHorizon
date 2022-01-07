<template>
	<div>
		<login-register v-show="page==='loginRegister'"
				@modalPage="(page, args) => $emit('modalPage', page, args)"/>
		<register-with-email v-show="page==='registerWithEmail'"
				@modalPage="(page, args) => $emit('modalPage', page, args)"/>
		<add-event v-show="page==='addEvent'"
				@modalPage="(page, args) => $emit('modalPage', page, args)"/>
		<settings v-show="page==='settings'"
				@modalPage="(page, args) => $emit('modalPage', page, args)"/>
		<aboutUs v-show="page==='aboutUs'"
				@modalPage="(page, args) => $emit('modalPage', page, args)"/>
	</div>
</template>
<script>
	import loginRegister from '@/views/loginRegister'
	import registerWithEmail from '@/views/registerWithEmail'
	import addEvent from '@/views/addEvent'
	import settings from '@/views/settings'
	import aboutUs from '@/views/aboutUs'
	export default {
		name: 'modalView',
		components: {
			loginRegister,
			registerWithEmail,
			addEvent,
			settings,
			aboutUs,
		},
		data () {
			return {
			}
		},
		props: {
			page: { default: null },
			args: { default: null },
		},
		mounted () {
			this.$emit('endLoading')
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>