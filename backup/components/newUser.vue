<template>
  <div>
    <h1 v-if="info !== null">{{info}}</h1>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Page2',
  data () {
    return {
      info: this.$route.params.info,
    }
  },
  methods: {
  },
}
</script>
<style scoped>
</style>
