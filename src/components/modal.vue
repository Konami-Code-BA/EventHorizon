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
	height: 100%;
	width: 100%;
	z-index: 99;
	background: rgba(0, 0, 0, 0.7);
}
</style>