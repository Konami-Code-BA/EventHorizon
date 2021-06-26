<template>
  <div id="app" class="app">
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<script>
	import store from '@/store'
	export default {
		name: 'App',
	}
</script>

<style>
	@media all {
		.app {
			font-family: 'Avenir', Helvetica, Arial, sans-serif;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
			color: black;
			font-size: 16px;
			max-width: 500px;
			width: 100%;
			margin-left: 50%;
			transform: translate(-50%, 0%);
		}
		/*[v-cloak] {
			display: none;
		}*/
		.fade-enter, .fade-leave-to {
			opacity: 0;
		}
		.logo {
			width: 50%;
			margin-left: 50%;
			transform: translate(-50%, 0%);
		}
		.box {
			width: 100%;
			display: flex;
			flex-flow: column wrap;
			align-content: space-between;
			justify-content: space-between;
		}
		.box-item {
			box-sizing: border-box;
			width: 100%;
			max-width: 100%;
			padding: 2px;
			height: 30px;
		}
		.box-center {
			text-align: center;
		}
		button {
			text-align: center !important;
			font-size: 16px;
			background-color: white;
			border: 1px solid black;
			box-shadow: 1px 1px black;
			border-radius: 5px;
			height: 30px;
			transition-duration: 0.3s;
			padding: 2px;
		}
		button:hover {
			font-weight: normal;
		}
		input[type=text], input[type=email], input[type=password] {
			font-size: 16px;
			border-radius: 3px;
			border: 1px solid black;
			height: 30px;
			padding: 5px;
			text-align: left;
		}
		input[type=text]:focus, input[type=email]:focus, input[type=password]:focus {
			border: 2px solid black;
			outline: none;
		}
		.half-border-button {
			border: none;
			background: none;
			box-shadow: 1px 1px black;
			transition-duration: 0.1s;
			width: 100%;
		}
		.half-border-button:active {
			font-weight: normal;
			box-shadow: none;
		}
		.no-border-button {
			border: none;
			background: none;
			box-shadow: none;
		}
		.hanolf-border-button:active {
			font-weight: normal;
		}
		.small-button {
			height: 19px !important;
		}
		.logout {
			text-align: left !important;
		}
		table {
			border-collapse: collapse;
		}
		td {
			padding: 0;
		}
		.close-button {
			border: none;
			background: none;
			height: 16px;
			padding: 0;
		}
		.header {
			display: flex;
			flex-direction: row;
			justify-content: space-between;
		}
	}
</style>
