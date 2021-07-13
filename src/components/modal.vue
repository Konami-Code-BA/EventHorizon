<template>
	<div>
		<div class="outside" v-on:click.prevent="$emit('closeModals')">
		</div>
		<div>
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
	position: fixed;
	top: 0;
	left: 0;
	height: 1000%;
	width: 1000%;
	z-index: 9999;
	background: rgba(0, 0, 0, 0.5);
	transform: translate(-50%, -50%);
}
.outside2 {
	z-index: 9999;
    background: rgba(0, 0, 0, 0.5);
    position: absolute !important;
    left: 0 !important;
    right: 0;
    top: 0;
    bottom: 0;
  	width: 100% !important;
  	max-width: 100% !important;
	transition: opacity .3s ease;
}
</style>