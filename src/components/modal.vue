<template>
	<div>
		<div class="outside" v-on:click.prevent="$emit('closeModals')">
		</div>
		<div class="contents">
			<slot name="contents">
			</slot>
		</div>
	</div>
</template>
<script>
	export default {
		name: 'modal',
		data () {
			return {
			}
		},
		mounted () {
		},
		methods: {
		}
	}
</script>
<style scoped>
.outside {
	z-index: 9999;
	position: fixed;
	width: 1000%;
	height: 1000%;
	margin-left: -500%;
	margin-top: -200%;
	background-color: rgba(0, 0, 0, .5);
	transition: opacity .3s ease;
}
.contents {
	position: fixed;
	z-index: 10000;
	background-color: #00022e;
	padding: inherit;
	width: inherit;
	text-align: inherit;
	left: inherit;
	right: inherit;
	top: inherit;
	left: inherit;
}
</style>