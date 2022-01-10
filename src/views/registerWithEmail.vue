<template>
	<div class="main" style="display: flex; flex-direction: column; justify-content: center">
		<register-with-email-internal style="width: 80%;" @startLoading="$emit('startLoading')"
			@endLoading="$emit('endLoading')" :next="'home'"/>
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
			this.$emit('endLoading')
		},
		watch: {
		},
		methods: {
		} // methods
	} // export
</script>
<style scoped>
</style>
