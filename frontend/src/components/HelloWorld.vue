<template>
  <div>
    <button v-on:click.prevent="getFriends()">Get Friends</button>
  </div>
</template>
<script>
import axios from 'axios'
import line from '@line/bot-sdk'
export default {
  name: 'HelloWorld',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
      input_username: null,
      username: null
    }
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

    goToPage2 () {
      this.$router.push({
        name: 'Page2',
        params: {
          info: this.input_username
        }
      })
    },

		async getFriends () {
			line.Client({
				channelAccessToken: this.token
			})
			.pushMessage(
				'<to>', {
					type: 'text',
					text: 'Hello World!!'
				})

				//.then((response) => {
				//	console.log(response)
				//})
				//.catch((err) => {
				//	console.log(err)
				//});
		}
  }
}
</script>
<style scoped>
</style>
