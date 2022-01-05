<template>
	<div>
		<login-register v-show="page==='loginRegister'" @modalPage="page => $emit('modalPage', page)"/>
		<register-with-email v-show="page==='registerWithEmail'" @modalPage="page => $emit('modalPage', page)"/>
		<add-event v-show="page==='addEvent'" @modalPage="page => $emit('modalPage', page)"/>
		<settings v-show="page==='settings'" @modalPage="page => $emit('modalPage', page)"/>
		<aboutUs v-show="page==='aboutUs'" @modalPage="page => $emit('modalPage', page)"/>
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
				history: []
			}
		},
		props: {
			page: { default: null },
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