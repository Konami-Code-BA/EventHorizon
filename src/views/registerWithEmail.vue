<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<register-with-email-internal style="width: 80%;" :next="'home'"/>
	</div>
</template>
<script>
	import registerWithEmailInternal from '@/components/registerWithEmailInternal.vue'
	export default {
		name: 'registerWithEmail',
		components: {
			registerWithEmailInternal,
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
