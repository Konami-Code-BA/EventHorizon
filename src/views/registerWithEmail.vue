<template>
		<div style="display: flex; flex-direction: column; justify-content: center">
			<div>
				<register-with-email-internal
					@startLoading="$emit('startLoading')"
					@endLoading="$emit('endLoading')"
					:next="'events'"
				/>
			</div>
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
