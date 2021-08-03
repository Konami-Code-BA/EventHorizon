<template>
	<div id="app">
		<div v-show="!loading" class="app">
			<div>
				<app-header @startLoading="loading=true" @endLoading="loading=false"/>
			</div>
			<div>
				<router-view @startLoading="loading=true" @endLoading="loading=false" :key="$route.fullPath"
						class="router"/>
			</div>
			<div>
				<app-footer @startLoading="loading=true" @endLoading="loading=false"/>
			</div>
		</div>
		<div class="loading" v-show="loading"></div>
	</div>
</template>

<script>
	import store from '@/store'
	import appHeader from '@/components/appHeader.vue'
	import appFooter from '@/components/appFooter.vue'
	export default {
		name: 'App',
		components: {
			appHeader,
			appFooter,
		},
		data () {
			return {
				loading: true,
			}
		},
	}
</script>

<style>
	@media all {
		@font-face {
			font-family: Futura;
			src: url(./assets/FuturaLT.woff);
		}
		html {
			-webkit-box-sizing: border-box;
			-moz-box-sizing: border-box;
			box-sizing: border-box;
		}
		*, *:before, *:after {
			-webkit-box-sizing: inherit;
			-moz-box-sizing: inherit;
			box-sizing: inherit;
		}
		body {
			font-family: Futura; /*Segoe UI*/
			color: #95c4ff; /*b4d5ff*/
			font-weight: 600; /*400=normal, 700=bold*/
			font-size: 16px;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
			background-color: #18002e; /*00033e 20003e*/
			margin: 0;
			padding: 0;
		}
		.app {
			position: fixed;
			display: flex;
			flex-direction: column;
			width: 100%;
		}
		.header-footer {
			position: fixed;
			color: inherit;
			width: 100%;
			display: flex;
			flex-direction: row;
			align-content: center;
			justify-content: space-around;
			height: 30px;
			border: 2px solid #95c4ff;
			background-color: #0b0015; /*00033e 18002e*/
		}
		.header {
			top: 0;
		}
		.router {
			position: fixed;
			top: 30px;
			bottom: 30px;
			overflow-y: auto;
			width: 100%;
		}
		.footer {
			bottom: 0;
		}
		.main {
			display: flex;
			flex-direction: column;
			align-items: center;
			width: 100%;
		}
		/*[v-cloak] {
			display: none;
		}*/
		.fade-enter, .fade-leave-to {
			opacity: 0;
		}
		.fade-enter-active, .fade-leave-active {
			transition: opacity .3s;
		}
		.icon {
			position: relative;
			height: 30px;
		}
		.box-height{
			height: 30px;
		}
		.box-center {
			text-align: center;
		}
		.button, .button:hover, .button:active, .button.pointer, .a, .a:hover, .a:active, .a.pointer {
			font-family: inherit;
			color: #ffe07a;
			font-weight: inherit;
			font-size: inherit;
			background-color: #5300e1;  /*000bff*/
			border: 1px solid #18002e;  /*18002e*/
			border-radius: 15px;
			height: 30px;
			cursor: pointer;
			padding: 0;
			padding-left: 3px;
			padding-right: 3px;
  			text-decoration: none;
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
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
			padding: 0;
			padding-left: 10px;
			outline: none !important;
		}
		::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  			color: #5841e9;
			font-weight: inherit;
		}
		.no-border-button, .no-border-button:hover, .no-border-button:active, .no-border-button.pointer {
			border: none;
			background: none;
			/*transition-duration: 0.1s;*/
			color: #ffe07a;
			cursor: pointer;
			height: 30px;
			padding: 0;
			font-family: inherit;
			font-weight: inherit;
			font-size: inherit;
  			text-decoration: none;
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
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
		.error-text {
			font-weight: 400; /*400=normal, 700=bold*/
			font-size: 12px;
			color: red;
		}

		/* LOADING SPINNER */

		/* Absolute Center Spinner */
		.loading {
			content: '';
			position: fixed;
			display: inline-block;
			left: 0;
			z-index: 1000;
			transform: translate(-5px, -5px);
			margin-left: 50%;
			margin-top: 50%;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
		}
		/* Transparent Overlay */
		.loading:before {
			content: '';
			display: inline-block;
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
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
			display: inline-block;
			font-size: 10px;
			width: 1em;
			height: 1em;
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

	/* SHAKE */
		
	.shake {
		animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
		transform: translate3d(0, 0, 0);
	}
	@keyframes shake {
		10%, 90% {
		transform: translate3d(-1px, 0, 0);
		}
		20%, 80% {
		transform: translate3d(2px, 0, 0);
		}
		30%, 50%, 70% {
		transform: translate3d(-4px, 0, 0);
		}
		40%, 60% {
		transform: translate3d(4px, 0, 0);
		}
	}
	}
</style>
