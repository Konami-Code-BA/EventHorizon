<template>
  <div>
		<div class="box">
			<br>
			<button v-on:click.prevent="goToRegistration()" class="box-item">REGISTER</button><br>
		</div>
	</div>
</template>
<script>
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'frontPage',
  data () {
    return {
			APIBaseUrl: '',
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
		goToRegistration () {
			this.$router.push(name='registration')
    },
  }
}
</script>
<style scoped>
</style>
