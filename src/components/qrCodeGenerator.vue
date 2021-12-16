<template>
	<div>
		<modal v-if="!closeModal" @closeModals="$emit('closeModals')">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="$emit('closeModals')" class="no-border-button">
						✖
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; getQr(url)" class="no-border-button">
						This Page QR
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; getQr(instagram)" class="no-border-button">
						Instagram QR
					</button>
				</div>
				<div>
					<button v-on:click.prevent="closeModal=true; getQr(line)" class="no-border-button">
						Line QR
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<modal v-if="image_name!=null" @closeModals="$emit('closeModals')">
			<div slot="contents" class="qr">
				<div>
				<a :href="image_file" :download="image_name" class="qr">
					<img class="qr-img" :src="image_file"/>
					<div class="qr-download" style="text-decoration: underline">
						⇩
					</div>
				</a>
				</div>
				<div class="qr-close">
					<button v-on:click.prevent="$emit('closeModals')" class="no-border-button" style="color: black">
						✖
					</button>
				</div>
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
				instagram: 'EventHorizonInstagramAccountQrCode.jpg',
				line: 'EventHorizonLineAccountQrCode.png',
				image_name: null,
				image_file: null,
				url: null,
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
		mounted () {
			this.url = window.location.href
		},
		methods: {
			t (w) { return translations.t(w) },
			async getQr (inp) { // when this isnt async, it works, but when its async, it outputs promise instead of what i want
				this.image_name = inp
				if (inp != this.url) {
					this.image_file = require('@/assets/' + this.image_name)
				} else {
					var QRCode = require('qrcode')
					this.image_file = await QRCode.toDataURL(this.url)
				}
			},
		}
	}
</script>
<style scoped>
	.modal {
		display: flex;
		flex-direction: column;
		align-items: center;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 80%;
		max-height: 80%;
		max-width: 300px;
		z-index: 101;
		pointer-events: auto;
	}
	.qr {
		display: flex;
		flex-direction: row;
		z-index: 101;
		pointer-events: auto;
		justify-content: flex-end;
		align-items: flex-start;
	}
	.qr-img {
		width: 100%;
		max-width: 300px;
	}
	.qr-close {
		position: fixed;
		height: 30px;
		width: 30px;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		z-index: 101;
		margin-right: 3px;
		color: black;
		border: none;
		background: none;
	}
	.qr-download {
		position: fixed;
		height: 30px;
		width: 30px;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		justify-content: flex-end;
		z-index: 101;
		margin-right: 3px;
		color: black;
		border: none;
		background: none;
		align-self: flex-end;
	}
</style>