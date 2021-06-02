<template>
  <div>
    <button v-on:click.prevent="line('consumption')">get number of messages sent so far</button><br>
		<br>
    <button v-on:click.prevent="line('broadcast')">broadcast to all</button><br>
		<br>
    <button v-on:click.prevent="line('push')">send to just mikey</button><br>
		<br>
    <button v-on:click.prevent="getuser()">getuser</button><br>
		<br>
    <button v-on:click.prevent="postuser()">postuser</button><br>
		<br>
		<input v-model="inp" placeholder="input here">
		<span v-if="response !== ''">{{response}}</span><br>
		<span v-if="error !== ''">{{error}}</span><br>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
  </div>
</template>
<script>
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'HelloWorld',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
			client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
			client_id: '1655871760',
			response: '',
			error: '',
			inp: '',
			APIBaseUrl: '',
    }
  },
	async mounted () {
		const csrftoken = JSON.parse('{"'+document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "')+'"}')['XSRF-TOKEN']
		axios.defaults.headers.common['X-CSRFToken'] = csrftoken
		console.log(process.env.NODE_ENV)
		if (process.env.NODE_ENV == 'development') {
			this.APIBaseUrl = 'http://127.0.0.1:8000'
		} else {
			this.APIBaseUrl = ''
		}
	}, 
  methods: {
    async getuser () {
      await axios
        .get(this.APIBaseUrl+'/api/user/?search=' + this.inp)
        .then(response => (this.response = response.data[0].date_joined))
        .catch(error => (console.log(error)))
      console.log(this.response)
    },

    async postuser () {
      await axios
        .post(this.APIBaseUrl+'/api/user/', {
          username: this.inp,
          password: '123'
        })
        .then(response => (this.response = response.data.date_joined))
        .catch(error => (console.log(error)))
      console.log(this.response)
    },

    async line (command) {
			this.response = ''
			this.error = ''
      await axios
				.post(this.APIBaseUrl+'/api/line/', {
					command: command,
					message: this.inp,
				})
        .then(response => {this.response = response['data'][response['data'].length-1]['response']})
        .catch(error => {this.error = error})
    },
  } // methods
} // export
</script>
<style scoped>
</style>
