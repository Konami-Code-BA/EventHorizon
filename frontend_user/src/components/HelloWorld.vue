<template>
  <div>
    <button v-on:click.prevent="getuser">Get user by username</button>
    <button v-on:click.prevent="postuser">Post new user with username</button><br>
    <input v-model="input_username" placeholder="input username"/><br>
    <button v-on:click.prevent="goToPage2">Go to Page 2</button>
    <h1 v-if="username !== null">{{username}}</h1>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  data () {
    return {
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
    }
  }
}
</script>
<style scoped>
</style>
