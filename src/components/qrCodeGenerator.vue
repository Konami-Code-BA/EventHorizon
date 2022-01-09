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
					<button v-on:click.prevent="closeModal=true; selectedQr = url; getQr()" class="button">
						This Page QR
					</button>
				</div>
				<div class="line-height"/>
				<div style="width: 100%">
					<button v-on:click.prevent="closeModal=true; selectedQr = instagram; getQr()"
							class="button">
						Instagram QR
					</button>
				</div>
				<div class="line-height"/>
				<div style="width: 100%">
					<button v-on:click.prevent="closeModal=true; selectedQr = line; getQr()" class="button">
						Line QR
					</button>
				</div>
				<div class="line-height"/>
			</div>
		</modal>
		<modal v-if="image_name!=null" @closeModals="$emit('closeModals')">
			<div slot="contents" class="qr">
				<div style="height: auto; width: 100%; display: flex; justify-content: center"
						v-on:click.prevent="$emit('closeModals')">
					<div class="qr-button" style="align-self: center">
						<button v-on:click.prevent="$emit('closeModals')" class="no-border-button x-button"
								style="color: black">
							✖
						</button>
					</div>
				</div>
				<div>
					<a :href="image_file" :download="image_name">
						<img class="qr-img" :src="image_file"/>
					</a>
				</div>
				<div style="height: 40px; width: 100%; display: flex; flex-direction: row; align-items: center; justify-content: center; margin-top: -5px;">
					<div style="height: 40px; width: 100%; z-index: 103; position: fixed"
							v-on:click.prevent="$emit('closeModals')"/>
					<a :href="image_file" :download="image_name" style="z-index: 105;">
						<!--div class="qr-button" style="text-decoration: underline; position: fixed; transform: translate(-50%,-12%)">
							⇩
						</div-->
						<div class="qr-button" style="text-decoration: underline;">
							⇩
						</div>
					</a>
					<button v-on:click.prevent="share()" class="qr-button">
						<img src="@/assets/blackShareIcon.png" class="icon"/>
					</button>
				</div>
			</div>
		</modal>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import modal from '@/components/modal'
	import store from '@/store.js'
	import f from '@/functions/functions.js'
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
				selectedQr: null,
			}
		},
		components: {
			modal,
		},
		props: {
		},
		computed: {
			url () {
				return f.domain+store.path
			},
		},
		watch: {
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async getQr () { // when this isnt async, it works, but when its async, it outputs promise instead of what i want
				this.image_name = this.selectedQr
				if (this.selectedQr != this.url) {
					this.image_file = require('@/assets/' + this.image_name)
				} else {
					let QRCode = require('qrcode')
					this.image_file = await QRCode.toDataURL(this.url)
					this.image_name = `EventHorizonQrCode${this.store.path.replace('/', '_')}.jpg`
				}
			},
			async share () {
				this.image_name = this.selectedQr
				if (this.selectedQr != this.url) {
					this.image_file = require('@/assets/' + this.image_name)
				} else {
					let QRCode = require('qrcode')
					this.image_file = await QRCode.toDataURL(this.url)
					this.image_name = `EventHorizonQrCode${this.store.path.replace('/', '_')}.jpg`
				}
				let image = await fetch(this.image_file)
				let blob = await image.blob()
				let file = new File([blob], this.image_name, { type: 'image/jpeg' })
				navigator.share({ files: [file] })
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