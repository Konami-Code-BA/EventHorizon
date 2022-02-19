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
			this.tryLineNewDevice()
		},
		watch: {
		},
		methods: {
			async redirectToLine() {
				this.store.loading = true
				let loginChannelId = await api.secretsApi('login-channel-id')
				let state = await api.secretsApi('new-random-secret')
				document.cookie = `state=${state};`
				let lineLoginRedirectUrl = f.createEncodedURL()
				lineLoginRedirectUrl += f.createUriForReturnFromLogin(f.currentPage, this.pageToReturnTo, true)
				let lineUrl = `https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=${loginChannelId}`
				lineUrl += `&redirect_uri=${lineLoginRedirectUrl}&state=${state}&prompt=consent&bot_prompt=aggressive`
				lineUrl += '&scope=profile%20openid'
				window.location.replace(lineUrl)
				this.store.loading = false
			},
			replaceAll(str, match, replace) {
				return str.replace(new RegExp(match, 'g'), () => replace);
			},
			async tryLineNewDevice() {
				this.store.loading = true
				if (document.cookie) {
					let allCookies = '{"' + this.replaceAll(this.replaceAll(document.cookie, '=', '": "'), '; ', '", "') + '"}'
					let stateCookie = JSON.parse(allCookies)['state']
					document.cookie = `state='';`
					if (f.currentPage && f.currentPage.args.code && stateCookie === f.currentPage.args.state) {
						let nextPage = f.createNextPageFromCurrentPage()
						let uri = f.createUriForReturnFromLogin(f.currentPage, nextPage, false)
						await api.lineNewDevice(f.currentPage.args.code, uri)
						f.goToPage(nextPage)
					}
				}
				this.store.loading = false
			},
		}
	}
</script>
<style scoped>
</style>