<template>
	<button v-on:click.prevent="redirectToLine()" class="button line-coloring"
			style="display: flex; flex-direction: row; align-items: center; justify-items: center;">
		<img src="@/assets/line.png" style="height: 27px;">
		<div>
			&nbsp;{{wording}}
		</div>
	</button>
</template>
<script>
	import store from '@/store.js'
	import f from '@/functions/functions.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'lineButton',
		components: {
		},
		data () {
			return {
				store: store,
			}
		},
		props: {
			pageToReturnTo: {},
			wording: {},
		},
		async mounted () {
		},
		watch: {
		},
		methods: {
			async redirectToLine() {
				this.store.loading = true
				let loginChannelId = await api.secretsApi('login-channel-id')
				let state = await api.secretsApi('new-random-secret')
				document.cookie = `state=${state};`
				let lineLoginRedirectUrl = 'https%3A%2F%2Fwww.eventhorizon.vip'
				if (process.env.PYTHON_ENV == 'development') {
					lineLoginRedirectUrl = 'http%3A%2F%2F127.0.0.1%3A8080'
				} else if (process.env.PYTHON_ENV == '"test"') {
					lineLoginRedirectUrl = 'https%3A%2F%2Fevent-horizon-test.herokuapp.com'
				}
				lineLoginRedirectUrl += f.createUriForReturnFromLogin(f.currentPage, this.pageToReturnTo, true)
				let lineUrl = `https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}`
				lineUrl += `&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive`
				lineUrl += '&scope=profile%20openid'
				window.location.replace(lineUrl)
			},
			replaceAll(str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async tryLineNewDevice() {
				let allCookies = '{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}'
				let stateCookie = JSON.parse(allCookies)['state']
				if (f.currentPage && f.currentPage.args.code && stateCookie === f.currentPage.args.state) {
					let nextPage = f.createNextPageFromCurrentPage(f.currentPage)
					let uri = f.createUriForReturnFromLogin(f.currentPage, nextPage, false)
					await api.lineNewDevice(f.currentPage.args.code, uri)
					f.goToPage(nextPage)
				}
			},
		}
	}
</script>
<style scoped>
</style>