<template>
	<div>
		<modal v-if="!closeModal">
			<div slot="contents" class="menu modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="$emit('closeModal')" class="no-border-button">
						✖
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; qrUrl='../assets/EventHorizonInstagramAccountQrCode.jpg'" class="no-border-button">
						Instagram QR
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; qrUrl='../assets/EventHorizonLineAccountQrCode.png'" class="no-border-button">
						Line QR
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; qrUrl='../assets/eventhorizonLogo.png'" class="no-border-button">
						Test
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<modal v-if="qrUrl!=''">
			<div slot="contents" class="qr modal">
				<img style="width: 200px; height: 200px; margin-left: 50%; transform: translate(-50%)" :src="qrUrl"/>
				<button style="margin-left: 50%; transform: translate(-50%)" v-on:click.prevent="$emit('closeModal')">✖</button>
			</div>
		</modal>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import modal from '@/components/modal'
	export default {
		name: 'qrCodeGenerator',
		data () {
			return {
				qrUrl: '',
				closeModal: false,
			}
		},
		components: {
			modal,
		},
		props: {
		},
		computed: {
		},
		watch: {
		},
		methods: {
			t (w) { return translations.t(w) },
			async showQrCode () {
				var QRCode = require('qrcode')
				await QRCode.toDataURL('eventhorizon.vip')
					.then(url => {
						this.qrUrl = url
					})
					.catch(err => {
						console.error('qr error:', err)
					})
				console.log(this.qrUrl)
			},
		}
	}
</script>
<style scoped>
	.modal {
		position: fixed;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		z-index: 101;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 80%;
		max-width: 300px;
		top: 40px;
	}
	.menu {
		right: 0;
	}
	.qr {
		top: 0;
		margin-left: 50%;
		transform: translate(-50%)
	}
</style>