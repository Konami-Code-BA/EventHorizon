<template>
	<div>
		<div class="outside" v-on:click.prevent="$emit('closeModals')">
		</div>
		<div class="inside">
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
	height: 100%;
	width: 100%;
	z-index: 99;
	background: rgba(255, 255, 255, 0.5);
}
.inside {
	position: fixed;
	top: 0;
	left: 0;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	height: 100%;
	z-index: 100;
	pointer-events: none;
}
</style>