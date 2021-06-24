<template>
	<div>
  	<div class="box">
			<div class="box-item logout">
				<button v-on:click.prevent="logout()" class="no-border-button"><small>LOGOUT</small></button><br>
			</div>
    	<img src="../assets/eventhorizon.png" class="logo"><br><br>
			<h1 v-if="thruParams !== null">Hello</h1>
			<h1 v-if="thruParams !== null">{{thruParams}}</h1>
  	</div>
	</div>
</template>
<script>
import store from '@/store'
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'pageTwo',
  data () {
    return {
      thruParams: this.$route.params.thruParams,
			response: '',
			error: '',
    }
  },
	mounted () {
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
  }
}
</script>
<style scoped>
</style>
