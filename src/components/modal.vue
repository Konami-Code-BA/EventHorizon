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
	position: absolute;
	top: 0;
	left: 0;
	height: 1000%;
	width: 1000%;
	z-index: 9999;
	background: rgba(0, 0, 0, 0.5);
	transform: translate(-50%, -50%);
}
</style>