<template>
  <div id="app">
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
		@font-face {
			font-family: Futura;
			src: url(./assets/FuturaLT.woff);
		}
		body {
			font-family: Futura; /*Segoe UI*/
			color: #d2e6ff;
			font-weight: 600; /*400=normal, 700=bold*/
			font-size: 16px;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
			background-color: #18002e; /*00033e 20003e*/
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
		button, button:hover, button:active {
			font-family: inherit;
			color: inherit;
			font-weight: inherit;
			font-size: inherit;
			font-size: 16px;
			background-color: #5300e1; /*000bff*/
			border: 1px solid #18002e;
			border-radius: 15px;
			height: 30px;
			transition-duration: 0.3s;
			padding: 10px;
			display: inline-flex;
			align-items: center; 
			justify-content: space-around;
		}
		input:-webkit-autofill, input:-webkit-autofill:hover, input:-webkit-autofill:focus,
		input:-webkit-autofill:active, input[type=text], input[type=email], input[type=password],
		input[type=text]:focus, input[type=email]:focus, input[type=password]:focus {
			font-family: inherit;
  			color: #5300e1;
  			-webkit-text-fill-color: #5300e1;
			font-weight: inherit;
			font-size: inherit;
			border-radius: 15px;
			border: 1px solid #18002e;
			background-color: #ffe07a;
 			-webkit-box-shadow: 0 0 0 30px #ffe07a inset;
			height: 30px;
			padding: 10px;
			display: inline-flex;
			align-items: center;
			outline: none !important;
		}
		::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  			color: #5841e9;
			font-weight: inherit;
		}
		.no-border-button, .no-border-button:hover, .no-border-button:active {
			border: none;
			background: none;
			/*transition-duration: 0.1s;*/
			width: 100%;
			height: inherit;
			color: #d2e6ff;
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
			color: #d2e6ff;
		}
		.header {
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			height: inherit;
			padding-bottom: 10px;
			color: #inherit;
		}
		.container {
			position: relative;
			display: inline-block;
			text-align: center;
		}
		.contained {
  			position: absolute;
			bottom: 50%;
			left: 0;
			right: 0;
			transform: translate(0, 50%);
		}
		.wide-img {
			width: 100%;
		}

		/* SPINNER */

		/* Absolute Center Spinner */
		.loading {
			position: fixed;
			z-index: 999;
			height: 2em;
			width: 2em;
			overflow: show;
			margin-left: 50%;
			margin-top: 50%;
		}
		/* Transparent Overlay */
		.loading:before {
			content: '';
			display: block;
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background-color: rgba(0,0,0,0.3);
		}
		/* :not(:required) hides these rules from IE9 and below */
		.loading:not(:required) {
			/* hide "loading..." text */
			font: 0/0 a;
			color: transparent;
			text-shadow: none;
			background-color: transparent;
			border: 0;
		}
		.loading:not(:required):after {
			content: '';
			display: block;
			font-size: 10px;
			width: 1em;
			height: 1em;
			margin-top: -0.5em;
			-webkit-animation: spinner 1500ms infinite linear;
			-moz-animation: spinner 1500ms infinite linear;
			-ms-animation: spinner 1500ms infinite linear;
			-o-animation: spinner 1500ms infinite linear;
			animation: spinner 1500ms infinite linear;
			border-radius: 0.5em;
			-webkit-box-shadow: rgba(0, 0, 0, 0.75) 1.5em 0 0 0, rgba(0, 0, 0, 0.75) 1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) 0 1.5em 0 0, rgba(0, 0, 0, 0.75) -1.1em 1.1em 0 0, rgba(0, 0, 0, 0.5) -1.5em 0 0 0, rgba(0, 0, 0, 0.5) -1.1em -1.1em 0 0, rgba(0, 0, 0, 0.75) 0 -1.5em 0 0, rgba(0, 0, 0, 0.75) 1.1em -1.1em 0 0;
			box-shadow: rgba(0, 0, 0, 0.75) 1.5em 0 0 0, rgba(0, 0, 0, 0.75) 1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) 0 1.5em 0 0, rgba(0, 0, 0, 0.75) -1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) -1.5em 0 0 0, rgba(0, 0, 0, 0.75) -1.1em -1.1em 0 0, rgba(0, 0, 0, 0.75) 0 -1.5em 0 0, rgba(0, 0, 0, 0.75) 1.1em -1.1em 0 0;
		}
		/* Animation */
		@-webkit-keyframes spinner {
			0% {
				-webkit-transform: rotate(0deg);
				-moz-transform: rotate(0deg);
				-ms-transform: rotate(0deg);
				-o-transform: rotate(0deg);
				transform: rotate(0deg);
			}
			100% {
				-webkit-transform: rotate(360deg);
				-moz-transform: rotate(360deg);
				-ms-transform: rotate(360deg);
				-o-transform: rotate(360deg);
				transform: rotate(360deg);
			}
		}
		@-moz-keyframes spinner {
			0% {
				-webkit-transform: rotate(0deg);
				-moz-transform: rotate(0deg);
				-ms-transform: rotate(0deg);
				-o-transform: rotate(0deg);
				transform: rotate(0deg);
			}
			100% {
				-webkit-transform: rotate(360deg);
				-moz-transform: rotate(360deg);
				-ms-transform: rotate(360deg);
				-o-transform: rotate(360deg);
				transform: rotate(360deg);
			}
		}
		@-o-keyframes spinner {
			0% {
				-webkit-transform: rotate(0deg);
				-moz-transform: rotate(0deg);
				-ms-transform: rotate(0deg);
				-o-transform: rotate(0deg);
				transform: rotate(0deg);
			}
			100% {
				-webkit-transform: rotate(360deg);
				-moz-transform: rotate(360deg);
				-ms-transform: rotate(360deg);
				-o-transform: rotate(360deg);
				transform: rotate(360deg);
			}
		}
		@keyframes spinner {
			0% {
				-webkit-transform: rotate(0deg);
				-moz-transform: rotate(0deg);
				-ms-transform: rotate(0deg);
				-o-transform: rotate(0deg);
				transform: rotate(0deg);
			}
			100% {
				-webkit-transform: rotate(360deg);
				-moz-transform: rotate(360deg);
				-ms-transform: rotate(360deg);
				-o-transform: rotate(360deg);
				transform: rotate(360deg);
			}
		}
	}
</style>
