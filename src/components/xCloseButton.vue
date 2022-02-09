<template>
	<div style="padding-bottom: 10px;">
		<button v-on:click.prevent="closeFunc()" class="no-border-button" style="height: auto; width: auto;">
			<img src="@/assets/blackXIcon.png" style="height: 25px; width: auto;" v-if="black">
			<img src="@/assets/xIcon.png" style="height: 25px; width: auto;" v-else>
		</button>
	</div>
</template>
<script>
	export default {
		name: 'xCloseButton',
		data () {
			return {
			}
		},
		props: {
			closeFunc: {},
			black : { default: false },
		},
		computed: {
		},
		async mounted () {
		},
		methods: {
		} // methods
	} // export
</script>
<style scoped>
</style>
