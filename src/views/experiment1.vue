<template>
	<div>
		<div class="main" id="page">
			<button v-on:click.prevent="sendWebhook()">trything</button>
			<input v-model="type" placeholder="type"/>
			<input v-model="text" placeholder="text"/>
			<img :src="imageone"/>
		</div>
	</div>
</template>
<script>
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'experiment1',
		components: {
		},
		data () {
			return {
				imageone: null,
				canvas: null,
				type: null,
				text: null,
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async trything2 () {
				let background = new Image()
				background.src = require('@/assets/pexels-photo-event1.jpg')
				let canvas = document.createElement('canvas')
				canvas.width = 200
				canvas.height = background.height / background.width * canvas.width
				let context = canvas.getContext('2d')
				await background.decode()
				context.drawImage(background, 0, 0, canvas.width, canvas.height)
				context.font = '10px Arial'
				context.fillStyle = 'black'
				context.fillText('hello world', 40, 40)
				let dataUrl = await canvas.toDataURL("image/png")
				this.imageone = dataUrl

				//let a = document.createElement("a")
				//let image_name = 'thing.png'
				//a.href = dataUrl
				//a.download = image_name
				//a.click()
			},
			async sendWebhook () {
				let mikeyId = await apiFunctions.secretsApiFunction('mikey-line-user-id')
				let events = [{
					'type': 'message',
					'message': {
						'type': 'text',
						'text': '. ' + this.type
					},
					'to': mikeyId,
					'reply': this.text
				}]
				await apiFunctions.sendWebhook({
					'events': events,
				})
			},
		} // methods
	} // export
</script>
<style scoped>
.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
  text-decoration: none;
}
</style>
