<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<email-password style="width: 80%;" action="registerWithEmail"/>
	</div>
</template>
<script>
	import emailPassword from '@/components/emailPassword.vue'
	export default {
		name: 'registerWithEmail',
		components: {
			emailPassword,
		},
		data () {
			return {
			}
		},
		async mounted () {
		},
		watch: {
		},
		methods: {
		} // methods
	} // export
</script>
<style scoped>
</style>
