<template>
	<div>
		<div class="main">
			<h1>experiment 2</h1>
			<button v-on:click.prevent="sendWebhook()">sendWebhook</button>
			<button v-on:click.prevent="lineConsumption()">lineConsumption</button>
			<button v-on:click.prevent="linePush()">linePush</button>
			<button v-on:click.prevent="lineBroadcast()">lineBroadcast</button>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'experiment2',
		components: {
		},
		data () {
			return {
				store: store,
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			async sendWebhook() {
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
			async lineConsumption() {
				await api.lineConsumption()
			},
			async linePush() {
				let data = {"to": "mikey", "messages": [{"type": "text", "text": "this is a thing"}]}
				await api.linePush(data)
			},
			async lineBroadcast() {
				await api.lineBroadcast()
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
