<template>
	<div>
		<div v-show="!loading">
			<menus-header @startLoading="loading=true" @endLoading="loading=false"/>
			<div>
				<register-with-email-internal @startLoading="loading=true" @endLoading="loading=false"/>
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="loading" v-show="loading"></div>
	</div>
</template>
<script>
	import menusHeader from '@/components/menusHeader.vue'
	import registerWithEmailInternal from '@/components/registerWithEmailInternal.vue'
	export default {
		name: 'registerWithEmail',
		components: {
			menusHeader,
			registerWithEmailInternal,
		},
		data () {
			return {
				loading: true,
			}
		},
		async mounted () {
			this.loading = false
		},
		watch: {
		},
		methods: {
		} // methods
	} // export
</script>
<style scoped>
</style>
