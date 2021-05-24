<template>
  <div>
    <button v-on:click.prevent="line_thing()">line_thing</button><br>
		<br>
		<a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
			token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
      input_username: 'mdsimeone',
      username: 'mdsimeone',
			client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
			client_id: '1655871760',
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

    async line_thing () {
      await axios
        .post('http://127.0.0.1:8000/api/line_thing/', {command: 'consumption'})
        .then(response => {console.log('response: ', response)})
        .catch(error => {console.log('error: ', error)})
    },
  } // methods
} // export
</script>
<style scoped>
</style>
