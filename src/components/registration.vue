<template>
	<div>
		<div class="box">
    	<img src="../assets/eventhorizon.png" class="logo"><br><br>
			<form v-on:keyup.enter="register()">
				<div class="box-item">USERNAME</div>
				<input v-model="usernameInput" placeholder="" ref="username" class="box-item"/><br>
				<br>
				<div class="box-item">EMAIL</div>
				<input v-model="emailInput" placeholder="" class="box-item"/><br>
				<br>
				<table class="box-item">
					<td style="text-align: left">PASSWORD</td>
					<td style="text-align: right"><small>SHOW</small><input v-model="showPassword" type="checkbox"></td>
				</table>
				<input v-model="passwordInput" placeholder="" :type="[showPassword ? 'text' : 'password']" class="box-item"/><br>
			</form><br>
			<button v-on:click.prevent="register()" class="box-item">REGISTER</button><br><br>
			<button v-on:click.prevent="goToLogin()" class="box-item">ALREADY REGISTERED? LOGIN</button><br><br>
			<span v-if="response !== ''">response:<br>{{response}}</span><br>
			<span v-if="error !== ''">error:<br>{{error}}</span>
			<br>
		</div>
		<button v-on:click.prevent="logout()" class="no-border-button footer">LOGOUT</button><br>
		<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
	</div>
</template>
<script>
import store from '@/store'
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'registration',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
			client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
			client_id: '1655871760',
			response: '',
			error: '',
			usernameInput: '',
			emailInput: '',
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
    async register () {
      await axios
        .post(this.APIBaseUrl+'/api/user/', {
					command: 'registration',
          username: this.usernameInput,
          email: this.emailInput,
          password: this.passwordInput,
					groups: [ 2 ],
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

		goToLogin () {
			this.$router.push({ name: 'login' })
		},
  } // methods
} // export
</script>
<style scoped>
.box {
	max-width: 80%;
	width: 300px;
	margin: auto;
}
.box-item {
	box-sizing: border-box;
	width: 100%;
	text-align: left;
	padding: 0;
}
table {
	border-collapse: collapse;
}
td {
	padding: 0;
}
button {
	text-align: center !important;
}
.no-border-button {
	border: none;
	background: none;
}
.footer {
	position: absolute;
	bottom: 5px;
	right: 5px;
}
</style>
