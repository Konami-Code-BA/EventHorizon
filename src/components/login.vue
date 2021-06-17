<template>
	<div>
		<div class="box">
			<div class="box-item logout">
				<button v-on:click.prevent="logout()" class="no-border-button"><small>LOGOUT</small></button><br>
			</div>
    	<img src="../assets/eventhorizon.png" class="logo"><br>
			<br>
			<button v-on:click.prevent="goToPage2()" class="box-item">GO TO PAGE 2</button><br>
			<br>
			<div class="box-item">USERNAME</div>
			<form v-on:keyup.enter="login()">
				<input v-model="usernameInput" placeholder="" ref="username" class="box-item"/><br>
				<br>
				<table class="box-item">
					<td style="text-align: left">PASSWORD</td>
					<td style="text-align: right"><small>SHOW</small><input v-model="showPassword" type="checkbox"></td>
				</table>
				<input v-model="passwordInput" placeholder="" :type="[showPassword ? 'text' : 'password']" class="box-item"/><br>
			</form>
			<br>
			<button v-on:click.prevent="login()" class="box-item">LOGIN</button><br>
			<br>
			<button v-on:click.prevent="login()" class="box-item">NOT REGISTERED YET?</button><br>
			<br>
			<span v-if="response !== ''">response:<br>{{response}}</span><br>
			<br>
			<span v-if="error !== ''">error:<br>{{error}}</span>
			<br>
		</div>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
	</div>
</template>
<script>
import store from '@/store'
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'login',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
			client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
			client_id: '1655871760',
			response: '',
			error: '',
			usernameInput: '',
			passwordInput: '',
			showPassword: false,
			APIBaseUrl: '',
    }
  },
	async mounted () {
    this.$refs.username.focus()
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
        .then(response => {
					this.response = response.data[0].date_joined
					this.error = ''
				})
        .catch(error => {
					this.response = ''
					this.error = error
				})
      console.log('response', this.response)
    },

    async login () {
      await axios
        .post(this.APIBaseUrl+'/api/user/', {
					command: 'login',
          username: this.usernameInput,
          password: this.passwordInput,
        })
        .then(response => {
					this.response = response.data[0]['username'] + ' just logged in'
					this.error = ''
					store.username = response.data[0]['username']
					store.groups = response.data[0]['groups']
				})
        .catch(error => {
					this.response = ''
					this.error = error
				})
      console.log('response', this.response)
    },

    async logout () {
			store.user = null
      await axios
        .post(this.APIBaseUrl+'/api/user/', {
					command: 'logout',
          username: store.username,
        })
        .then(response => {
					this.response = response.data[0]['username'] + ' just logged out'
					this.error = ''
					store.username = null
					store.groups = []
					location.reload()
				})
        .catch(error => {
					this.response = ''
					this.error = error
				})
      console.log('response', this.response)
    },

    async line (command) {
			this.response = ''
			this.error = ''
      await axios
				.post(this.APIBaseUrl+'/api/line/', {
					command: command,
					message: this.inp,
				})
        .then(response => {
					this.response = response['data'][response['data'].length-1]['response']
					this.error = ''
				})
        .catch(error => {
					this.response = ''
					this.error = error
				})
    },

		goToPage2 () {
			this.$router.push({ name: 'pageTwo', params: { thruParams: 'this was sent from the login page' } })
		},
  } // methods
} // export
</script>
<style scoped>
</style>
