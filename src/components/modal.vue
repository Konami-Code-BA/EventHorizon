<template>
	<div>
		<div class="modal-outside" v-on:click.prevent="closeModals()"
				:style="[haveBackground ? {} : {background: 'none'}]"/>
		<div class="modal-inside">
			<slot name="contents">
			</slot>
		</div>
	</div>
</template>
<script>
	import xCloseButton from '@/components/xCloseButton.vue'
	import f from '@/functions/functions.js'
	import store from '@/store'
	export default {
		name: 'modal',
		components: {
			xCloseButton,
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
			haveBackground: { default: true },
		},
		created () {
			this.store.modalBack = true
			let closeModals = this.closeModals
			let goBack = f.goBack
			window.removeEventListener('popstate', goBack)
			window.addEventListener('popstate', closeModals)
		},
		methods: {
			closeModals () {
				let closeModals = this.closeModals
				let goBack = f.goBack
				window.removeEventListener('popstate', closeModals)
				window.addEventListener('popstate', goBack)
				this.store.modalBack = false
				this.$emit('closeModals')
			}
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