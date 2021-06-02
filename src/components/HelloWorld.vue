<template>
  <div>
    <button v-on:click.prevent="line('consumption')">get number of messages sent so far</button><br>
		<br>
    <button v-on:click.prevent="line('broadcast')">broadcast to all</button><br>
		<br>
    <button v-on:click.prevent="line('push')">send to just mikey</button><br>
		<br>
		<input v-model="message" placeholder="message">
		<span v-if="response !== ''">{{response}}</span><br>
		<span v-if="error !== ''">{{error}}</span><br>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
  </div>
</template>
<script>
import axios from 'axios'
//axios.defaults.xsrfHeaderName = "X-CSRFToken";
//axios.defaults.withCredentials = true
export default {
  name: 'HelloWorld',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
      input_username: 'mdsimeone',
      username: 'mdsimeone',
			client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
			client_id: '1655871760',
			response: '',
			error: '',
			message: '',
    }
  },
	async mounted () {
		const csrftoken = JSON.parse('{"'+document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "')+'"}')['XSRF-TOKEN']
		axios.defaults.headers.common['x-csrftoken'] = csrftoken;
		console.log(process.env.NODE_ENV)
	}, 
  methods: {
    async getuser () {
      await axios
        .get('http://127.0.0.1:8000/api/user/?search=' + this.input_username)
        .then(response => (this.username = response.data[0].username))
        .catch(error => (console.log(error)))
      console.log(this.username)
    },

    async postuser () {
      await axios
        .post('http://127.0.0.1:8000/api/user/', {
          username: this.input_username,
          password: '123'
        })
        .then(response => (this.username = response.data.username))
        .catch(error => (console.log(error)))
      console.log(this.username)
    },

    async line (command) {
			this.response = ''
			this.error = ''
			let baseUrl = ''
			if (process.env.NODE_ENV == 'development') {
				baseUrl = 'http://127.0.0.1:8000'
			} else {
				baseUrl = ''
			}
      await axios
				.post(baseUrl+'/api/line/', {
					command: command,
					message: this.message,
				})
        .then(response => {this.response = response['data'][response['data'].length-1]['response']})
        .catch(error => {this.error = error})
    },
  } // methods
} // export
</script>
<style scoped>
</style>
