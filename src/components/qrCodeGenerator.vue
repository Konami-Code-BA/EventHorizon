<template>
	<div>
		<modal v-if="!closeModal" @closeModals="$emit('closeModals')">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end; padding-bottom: 5px; padding-bottom: 5px;">
					<button v-on:click.prevent="$emit('closeModals')" class="no-border-button x-button">
						✖
					</button>
				</div>
				<div style="width: 100%">
					<button v-on:click.prevent="closeModal=true; getQr(url)" class="button">
						This Page QR
					</button>
				</div>
				<div class="line-height"></div>
				<div style="width: 100%">
					<button v-on:click.prevent="closeModal=true; getQr(instagram)" class="button">
						Instagram QR
					</button>
				</div>
				<div class="line-height"></div>
				<div style="width: 100%">
					<button v-on:click.prevent="closeModal=true; getQr(line)" class="button">
						Line QR
					</button>
				</div>
				<div class="line-height"></div>
			</div>
		</modal>
		<modal v-if="image_name!=null" @closeModals="$emit('closeModals')">
			<div slot="contents" class="qr">
				<div style="height: auto; width: 100%; display: flex; justify-content: center"
						v-on:click.prevent="$emit('closeModals')">
					<div class="qr-button" style="align-self: center">
						<button v-on:click.prevent="$emit('closeModals')" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<div>
					<a :href="image_file" :download="image_name">
						<img class="qr-img" :src="image_file"/>
					</a>
				</div>
				<div style="height: 40px; width: 100%; display: flex; flex-direction: column; align-items: center">
					<div style="height: 40px; width: 100%; z-index: 103; position: fixed"
							v-on:click.prevent="$emit('closeModals')"/>
					<a :href="image_file" :download="image_name">
						<div class="qr-button" style="text-decoration: underline; position: fixed">
							⇩
						</div>
					</a>
				</div>
			</div>
		</modal>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import modal from '@/components/modal'
	import store from '@/store.js'
	export default {
		name: 'qrCodeGenerator',
		data () {
			return {
				store: store,
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
			this.url = window.location.protocol + '//' + window.location.host + this.store.path
			console.log(this.url)
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
	.qr {
		display: flex;
		flex-direction: column;
		z-index: 101;
		pointer-events: auto;
		justify-content: center;
		align-items: center;
	}
	.qr-img {
		width: 100%;
		max-width: 300px;
		border: 2px solid black;
		border-radius: 7px;
	}
	.qr-button {
		height: 40px;
		width: 40px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 105;
		color: black;
		border-radius: 7px;
		border: 2px solid black;
		background: white;
		align-self: center;
	}
	.button {
		width: 100%;
	}
</style>