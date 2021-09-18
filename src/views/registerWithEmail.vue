<template>
	<div class="main" style="justify-content: center">
		<div>
			<register-with-email-internal
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"
			/>
		</div>
	</div>
</template>
<script>
	import appHeader from '@/components/appHeader.vue'
	import registerWithEmailInternal from '@/components/registerWithEmailInternal.vue'
	export default {
		name: 'registerWithEmail',
		components: {
			appHeader,
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
