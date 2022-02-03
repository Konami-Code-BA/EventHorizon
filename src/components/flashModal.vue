<template>
	<div v-if="showFlashModal" class="flash-modal" :class="[nonCenter ? 'noncentered' : 'centered', flashModalClass]">
		{{ text }}
	</div>
</template>
<script>
	export default {
		name: 'flashModal',
		props: {
			time: { default: 700 }, // .7 seconds
			text: {},
			nonCenter: { default: false }
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
		color: black;
		font-size: 72px;
		background-color: rgba(255, 255, 255, .5);
		z-index: 90000;
		width: 90%;
		text-align: center;
	}
	.centered {
		position: fixed;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
	}
	.noncentered {
		position: absolute;
	}
</style>
