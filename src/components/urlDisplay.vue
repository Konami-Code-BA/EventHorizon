<template>
	<div>
		<modal @closeModals="$emit('closeModals')">
			<div slot="contents" class="modal">
				<div style="align-self: flex-end; padding-bottom: 5px; padding-bottom: 5px;">
					<button v-on:click.prevent="$emit('closeModals')" class="no-border-button x-button">
						✖
					</button>
				</div>
				<div style="width: 100%; display: flex; flex-direction: row; align-items: center">
					<button v-on:click.prevent="copyToClipboard()" class="button" style="border: none;">
						<img src="@/assets/copyIcon.png" class="icon"/>
					</button>
						{{url}}
				</div>

				<div class="line-height"/>

				<button v-on:click.prevent="share()" class="button">
					<img src="@/assets/shareIcon.png" class="icon"/>
				</button>
			</div>
		</modal>
		<div v-if="showFlashModal" :class="flashModalClass" class="success-modal">
			{{ t('COPIED!') }}
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import modal from '@/components/modal'
	import f from '@/functions/functions.js'
	export default {
		name: 'urlDisplay',
		components: {
			modal,
		},
		data () {
			return {
				store: store,
				showFlashModal: false,
				flashModalClass: null,
			}
		},
		computed: {
			url () {
				return f.currentUrl
			},
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async copyToClipboard () {
				navigator.clipboard.writeText(this.url)
				//// if the above fails on some browser, this is supposed to work. maybe use both if the first fails
				//let textArea = document.createElement("textarea")
				//textArea.value = this.url
				//textArea.hidden = true  // not sure about this line or not
				//document.body.appendChild(textArea)
				//textArea.select()
				//document.execCommand('copy')

				await f.flashModal(this)  // flash copied! modal
			},
			share () {
				navigator.share({url: this.url})
			},
		} // methods
	} // export
</script>
<style scoped>
	.success-modal {
		position: fixed;
		color: white;
		font-size: 32px;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		background-color: rgba(0, 0, 0, .5);
		z-index: 1000;
	}
</style>
