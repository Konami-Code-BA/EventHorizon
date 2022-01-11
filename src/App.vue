<template>
	<div id="app">
		<div v-show="!store.loading" class="app" v-if="initialLoadCompleted">
			<app-header/>
			<router-view
					:key="$route.fullPath"
					class="router"
					v-show="page === 'home'"/>
			<modal-view
					class="router"
					v-show="page != 'home'"
					:key="page"/>
			<app-footer/>
		</div>
		<div class="loading" v-if="store.loading"/>
		<opening-logo class="opening" :class="fadeOutClass" v-if="opening"/>
	</div>
</template>

<script>
	import store from '@/store'
	import appHeader from '@/components/appHeader.vue'
	import modalView from '@/views/modalView.vue'
	import appFooter from '@/components/appFooter.vue'
	import openingLogo from '@/views/openingLogo.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'App',
		components: {
			appHeader,
			modalView,
			appFooter,
			openingLogo,
		},
		data () {
			return {
				store: store,
				opening: true,
				fadeOutClass: null,
				page: null,
				initialLoadCompleted: false,
			}
		},
		async created () {
			// back button setup
			window.addEventListener('popstate', () => { f.goBack() })
			
			// user auto-login from cookies
			if (store.user.groups[0] === 100) { // if never logged in, not even to visitor account, login
				console.log(process.env.PYTHON_ENV)
				await api.login({})
				if (store.user.groups.includes(3)) {
					console.log('visitor')
				} else {
					console.log('existing user')
				}
			}

			// get events
			await f.getEvents()

			// google maps
			if (!document.getElementById('mapscrip')) {
				let scrip = document.createElement('script')
				scrip.id = 'mapscrip'
				scrip.type = 'text/javascript'
				let apiKey = await api.secretsApi('google-maps-api-key')
				scrip.src = `https://maps.googleapis.com/maps/api/js?v=weekly&key=${apiKey}&callback=initMap`
				document.head.appendChild(scrip)
			}

			this.initialLoadCompleted = true
			store.loading = false
		},
		async mounted () {
			// openingLogo
			await new Promise(r => setTimeout(r, 2000))
			this.fadeOutClass = 'fade-out'
			await new Promise(r => setTimeout(r, 1000))
			this.opening = false
			this.fadeOutClass = null
		},
		watch: {
			'store.pages' () {
				this.page = f.currentPage.page
				window.history.pushState({ path: f.currentUrl }, '', f.currentUrl)
			},
		},
		methods: {
			t (w) { return translations.t(w) },
			checkLoading () {

			},
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
			height: 100%;
		}
		.header {
			position: relative;
			top: 0;
			z-index: 2;
		}
		.router {
			position: relative;
			overflow-x: hidden;
			overflow-y: hidden;
			width: 100%;
			height: 100%;
			padding-left: 10px;
			padding-right: 10px;
			z-index: 1;
		}
		.footer {
			position: relative;
			bottom: 0;
			z-index: 2;
		}
		.main {
			display: flex;
			flex-direction: column;
			align-items: center;
			width: 100%;
			height: 100%;
			z-index: 1;
		}
		/*[v-cloak] {
			display: none;
		}*/
		.icon {
			height: 20px;
			vertical-align: bottom;
		}
		.line-height{
			height: 30px;
		}
		.button, .button:hover, .button:active, .button.pointer, .a, .a:hover, .a:active, .a.pointer {
			font-family: inherit;
			color: #ffe07a;  /*ffe07a*/
			font-weight: inherit;
			font-size: inherit;
			background-color: transparent;  /*5300e1, 000bff*/
			border: 2px solid #ffe07a;  /*18002e*/
			border-radius: 15px;
			height: 30px;
			cursor: pointer;
			padding-top: 0;
			padding-bottom: 0;
			padding-left: 10px;
			padding-right: 10px;
  			text-decoration: none;
			width: auto;
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
			white-space: nowrap;
		}
		.button:disabled, .button[disabled] {
			font-family: inherit;
			color: #808080;  /*ffe07a*/
			font-weight: inherit;
			font-size: inherit;
			background-color: transparent;  /*5300e1, 000bff*/
			border: 2px solid #808080;  /*18002e*/
			border-radius: 15px;
			height: 30px;
			cursor: pointer;
			padding-top: 0;
			padding-bottom: 0;
			padding-left: 10px;
			padding-right: 10px;
  			text-decoration: none;
			width: auto;
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
			white-space: nowrap;
		}
		input:-webkit-autofill, input:-webkit-autofill:hover, input:-webkit-autofill:focus,
		input:-webkit-autofill:active, input[type=text], input[type=email], input[type=password],
		input[type=text]:focus, input[type=email]:focus, input[type=password]:focus, textarea {
			font-family: inherit;
  			color: #18002e;
  			-webkit-text-fill-color: #18002e;
			font-weight: inherit;
			font-size: inherit;
			border-radius: 15px;
			border: none;
			background-color: #ffe07a;
 			-webkit-box-shadow: 0 0 0 30px #ffe07a inset;
			height: 30px;
			padding: 0;
			padding-left: 10px;
			outline: none !important;
			width: 100%;
		}
		form {
			display: flex;
			flex-direction: column;
			width: 100%;
		}
		.modal {
			display: flex;
			flex-direction: column;
			align-items: center;
			background-color: #18002e;
			border: 2px solid #ffe07a;
			border-radius: 15px;
			padding: 20px;
			width: 80%;
			max-height: 80%;
			max-width: 300px;
			z-index: 101;
			pointer-events: auto;
		}
		::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  			color: #5841e9;
			font-weight: inherit;
		}
		.no-border-button, .no-border-button:hover, .no-border-button:active, .no-border-button.pointer {
			border: none;
			background: none;
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
		.x-button {
			/*color: red;*/
			font-size: 24px;
		}
		.viewer {
			width: 100%;
			height: 100%;
			margin-bottom: 5px;
			border: 2px solid rgba(255, 255, 255, .3);
			border-bottom-left-radius: 7px;
			border-bottom-right-radius: 7px;
			border-top-left-radius: 7px;
			border-top-right-radius: 7px;
			overflow-x: hidden;
			overflow-y: hidden;
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
		::-webkit-scrollbar {
			-webkit-appearance: none;
			width: 10px;
			height: 10px;
		}
		::-webkit-scrollbar-thumb {
			border-radius: 4px;
			background-color: rgba(0, 0, 0, .5);
			border: 2px solid rgba(255, 255, 255, .3);
		}
		.opening {
			position: fixed;
			z-index: 100000;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: #18002e;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
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
			-webkit-box-shadow: rgba(255, 255, 255, .7) 1.5em 0 0 0, rgba(255, 255, 255, .7) 1.1em 1.1em 0 0, rgba(255, 255, 255, .7) 0 1.5em 0 0, rgba(255, 255, 255, .7) -1.1em 1.1em 0 0, rgba(255, 255, 255, .7) -1.5em 0 0 0, rgba(0, 0, 0, 0.5) -1.1em -1.1em 0 0, rgba(255, 255, 255, .7) 0 -1.5em 0 0, rgba(255, 255, 255, .7) 1.1em -1.1em 0 0;
			box-shadow: rgba(255, 255, 255, .7) 1.5em 0 0 0, rgba(255, 255, 255, .7) 1.1em 1.1em 0 0, rgba(255, 255, 255, .7) 0 1.5em 0 0, rgba(255, 255, 255, .7) -1.1em 1.1em 0 0, rgba(255, 255, 255, .7) -1.5em 0 0 0, rgba(255, 255, 255, .7) -1.1em -1.1em 0 0, rgba(255, 255, 255, .7) 0 -1.5em 0 0, rgba(255, 255, 255, .7) 1.1em -1.1em 0 0;
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

		/* FADE */

		/*.fade-start-out {
			opacity: 0;
		}
		.fade-in {
			transition: opacity 3s;
			opacity: 1;
		}*/
		.fade-out {
			opacity: 0;
			transition: opacity 1s;
		}
	}
</style>
