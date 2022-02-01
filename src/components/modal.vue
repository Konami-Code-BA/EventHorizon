<template>
	<div>
		<div class="modal-outside" v-on:click.prevent="$emit('closeModals')">
		</div>
		<div class="modal-inside">
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
.modal-outside {
	position: fixed;
	top: 0;
	left: 0;
	height: 100%;
	width: 100%;
	z-index: 99;
	background: rgba(0, 0, 0, 0.5);
}
.modal-inside {
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
	overflow-y: hidden;
	overflow-x: hidden;
}
</style>