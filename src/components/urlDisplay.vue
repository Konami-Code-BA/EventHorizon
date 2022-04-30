<template>
	<div>
		<modal @closeModals="$emit('closeModals')" ref="urlDisplayModal">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {$refs.urlDisplayModal.closeModals()}" style="align-self: flex-end;"/>
				<div style="width: 100%; display: flex; flex-direction: row; align-items: center">
					<button v-on:click.prevent="copyToClipboard()" class="button" style="border: none;"> 
						<img src="@/assets/copyIcon.png" class="icon"/>
					</button>
					<div style="width: 90%; overflow-wrap: break-word;">{{url}}</div>
				</div>

				<div class="line-height"/>

				<button v-on:click.prevent="share()" class="button" v-if="navigate">
					<img src="@/assets/shareIcon.png" class="icon"/>
				</button>
			</div>
		</modal>
		<flash-modal :text="t('COPIED!')" ref="flashCoppied"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import modal from '@/components/modal'
	import f from '@/functions/functions.js'
	import flashModal from '@/components/flashModal.vue'
	import xCloseButton from '@/components/xCloseButton.vue'
	export default {
		name: 'urlDisplay',
		components: {
			modal,
			flashModal,
			xCloseButton,
		},
		data () {
			return {
				store: store,
				navigate: navigator.share,
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
				const promise1 = new Promise((resolve, reject) => {
					resolve(this.url)
				})
				promise1.then((value) => {
					navigator.clipboard.writeText(value)
					if (typeof NativeAndroid !== 'undefined') {
						NativeAndroid.copyToClipboard(value)
					}
				})
				//// if the above fails on some browser, this is supposed to work. maybe use both if the first fails
				// let textArea = document.createElement("textarea")
				// textArea.value = this.url
				// textArea.hidden = true  // not sure about this line or not
				// document.body.appendChild(textArea)
				// textArea.select()
				// document.execCommand('copy')

				await this.$refs.flashCoppied.flashModal()
			},
			share () {
        		const promise1 = new Promise((resolve, reject) => {
          			resolve(this.url);
        		})
        		promise1.then((value) => {
					navigator.share({url: value})
				})
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
