<template>
</template>
<script>
	export default {
		name: 'temp',
		components: {
		},
		data () {
			return {
			}
		},
		props: {
		},
		mounted () {
			this.$router.push({ name: 'home', params: this.$route.params })
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>