<template>
	<div>
		<div class="main" id="page">
			<button v-on:click.prevent="sendWebhook()">sendWebhook</button>
			<button v-on:click.prevent="linePush()">linePush</button>
			<input v-model="type" placeholder="type"/>
			<input v-model="text" placeholder="text"/>
			<button v-on:click.prevent="saveImage()">saveImage</button>
			<input type="file" accept="image/*" @change="(e) => {imageFile = e.target.files[0]}">
			<input v-model="getimgid" placeholder="id#"/>
			<button v-on:click.prevent="getImage()">getImage</button>
			<img :src="imagetwo" style="width: 100px; height: 100px;"/>
			<!--button v-on:click.prevent="makeImage()">makeImage</button-->    <!--for makeImage()-->
			<!--img :src="imageone"/-->    <!--for makeImage()-->
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
				imagetwo: null,
				canvas: null,
				type: null,
				text: null,
				imageFile: null,
				getimgid: null,
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			//async makeImage () {  // this was finished but i need to do it in backend afterall so leave unused
			//	let background = new Image()
			//	background.src = require('@/assets/pexels-photo-event1.jpg')
			//	let canvas = document.createElement('canvas')
			//	canvas.width = 200
			//	canvas.height = background.height / background.width * canvas.width
			//	let context = canvas.getContext('2d')
			//	await background.decode()
			//	context.drawImage(background, 0, 0, canvas.width, canvas.height)
			//	context.font = '10px Arial'
			//	context.fillStyle = 'black'
			//	context.fillText('hello world', 40, 40)
			//	let dataUrl = await canvas.toDataURL("image/png")
			//	this.imageone = dataUrl

			//	//let a = document.createElement("a")  // uncomment this part to save the image rather than just display
			//	//let image_name = 'thing.png'
			//	//a.href = dataUrl
			//	//a.download = image_name
			//	//a.click()
			//},
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
			async linePush () {
				let data = {"to": "mikey", "messages": [{"type": "text", "text": "this is a thing"}]}
				await apiFunctions.linePush(data)
			},
			async saveImage () {
				let formData = new FormData();
				formData.append("file", this.imageFile)
				await apiFunctions.saveImage(formData)
			},
			async getImage () {
				let result = await apiFunctions.getImage(this.getimgid)
				let imgUrl = apiFunctions.baseUrl ? apiFunctions.baseUrl : window.location.hostname + result.image
				console.log(imgUrl)
				this.imagetwo = imgUrl
			}
		} // methods
	} // export
</script>
<style scoped>
.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
  text-decoration: none;
}
</style>
