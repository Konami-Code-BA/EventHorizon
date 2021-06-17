<template>
  <div id="app" v-cloak>
    <img src="./assets/eventhorizon.png" class="logo">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
	#app {
		font-family: 'Avenir', Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: #2c3e50;
		margin-top: 60px;
	}

	/*[v-cloak] {display: none}*/
	[v-cloak] > * { display:none }
	[v-cloak]::before { content: "loading…" }

	.logo {
		max-width: 80%;
		width: 300px;
		height: 100%;
	}

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

	button {
		text-align: center !important;
	}

</style>
