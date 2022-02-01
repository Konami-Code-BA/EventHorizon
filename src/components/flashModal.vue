<template>
	<div v-if="showFlashModal" :class="flashModalClass" class="flash-modal">
		{{ text }}
	</div>
</template>
<script>
	export default {
		name: 'flashModal',
		props: {
			time: { default: 700 }, // .7 seconds
			text: {},
		},
		data () {
			return {
				showFlashModal: false,
				flashModalClass: null,
			}
		},
		mounted () {
		},
		methods: {
			async flashModal() {
				this.showFlashModal = true
				await new Promise(r => setTimeout(r, this.time))
				this.flashModalClass = 'fade-out'
				await new Promise(r => setTimeout(r, 1000)) // 1 seconds
				this.showFlashModal = false
				this.flashModalClass = null
			},
		} // methods
	} // export
</script>
<style scoped>
	.flash-modal {
		position: fixed;
		color: white;
		font-size: 24px;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		background-color: rgba(0, 0, 0, .9);
		z-index: 90000;
		width: 90%;
		text-align: center;
	}
</style>
