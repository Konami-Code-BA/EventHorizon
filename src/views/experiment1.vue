
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
			<img style="width: 100px; height: 100px;" :src="imagetwo"/>
			<button v-on:click.prevent="sendEmail()">sendEmail</button>
			<!--button v-on:click.prevent="makeImage()">makeImage</button-->    <!--for makeImage()-->
			<!--img :src="imageone"/-->    <!--for makeImage()-->
			<button v-on:click.prevent="fbLogin()">fbLogin</button>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'experiment1',
		components: {
		},
		data () {
			return {
				store: store,
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
			let js = document.createElement('script')
			js.id = 'facebook-jssdk'
			js.src = 'https://connect.facebook.net/en_US/sdk.js'
			await document.head.appendChild(js)
			window.fbAsyncInit = async () => {
				await window.FB.init({
					appId: '467874544824216', //You will need to change this
					cookie: false, // This is important, it's not enabled by default
					version: 'v13.0'
				})
			}
		},
		methods: {
			t (w) { return translations.t(w) },
			////this was finished but i need to do it in backend afterall so leave unused
			//async makeImage () {
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
				let mikeyId = await api.secretsApi('mikey-line-user-id')
				let events = [{
					'type': 'message',
					'message': {
						'type': 'text',
						'text': '. ' + this.type
					},
					'to': mikeyId,
					'reply': this.text
				}]
				await api.sendWebhook({
					'events': events,
				})
			},
			async linePush () {
				let data = {"to": "mikey", "messages": [{"type": "text", "text": "this is a thing"}]}
				await api.linePush(data)
			},
			async saveImage () {
				let formData = new FormData()
				formData.append('file', this.imageFile)
				formData.append('event_pk', 87)  // this.event.id
				let result = await api.saveImage(formData)
				return result.id
			},
			async getImage () {
				let formData = new FormData()
				formData.append('event_pk', 87)  // this.event.id
				let result = await api.getImage(this.getimgid, formData)
				this.imagetwo = "data:image/jpg;base64," + result
			},
			async sendEmail() {
				await api.sendEmail()
			},
			async fbLogin () {
				window.FB.getLoginStatus(response => {
					if (response.status === 'connected') {
						console.log('ALREADY LOGGED IN')
					} else {
						console.log('LOGGING IN')
						FB.login(response => {
							if (response.authResponse) {
								console.log('LOGIN SUCCESS')
								console.log(response)
								console.log(document.cookie)
								// Now you can redirect the user or do an AJAX request to
								// a PHP script that grabs the signed request from the cookie.
							} else {
								console.log('LOGIN FAILED')
							}
						})
					}
				})
			}
		} // methods
	} // export
</script>
<style scoped>
.maps-link:link, .maps-link:visited, .maps-link:hover, .maps-link:active {
  text-decoration: none;
}
</style>
