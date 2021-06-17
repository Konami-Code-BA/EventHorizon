<template>
  <div>
    <h1 v-if="thruParams !== null">Hello</h1>
    <h1 v-if="thruParams !== null">{{thruParams}}</h1>
  </div>
</template>
<script>
import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
export default {
  name: 'pageTwo',
  data () {
    return {
      thruParams: this.$route.params.thruParams,
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
  }
}
</script>
<style scoped>
</style>
