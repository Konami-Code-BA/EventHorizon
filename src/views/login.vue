<template>
	<div>
		<div v-if="!loading">
			<div class="box">
				<menus-header :isLoginPage="true"/>
				<br>
				<form v-on:keyup.enter="login()">
					<input :placeholder="t('USERNAME')" v-model="usernameInput" type="text" class="box-item"
						id="username"/><br>
					<br>
					<div style="display: flex;">
						<input :placeholder="t('PASSWORD')" v-model="passwordInput"
							:type="[showPassword ? 'text' : 'password']" class="box-item" style="flex-grow: 4;"
							id="password"/>
						<button v-on:click.prevent="showPassword = !showPassword" class="box-item" style="width: 60px"
							id="show">
							<small v-if="!showPassword">{{ t('SHOW') }}</small>
							<small v-else>{{ t('HIDE') }}</small>
						</button><br>
					</div>
				</form>
				<br>
				<div>
				<button v-on:click.prevent="login()" class="box-item">{{ t('LOGIN') }}</button><br>
				</div>
				<br>
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="box" v-else>
			Loading...
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'login',
		components: {
			menusHeader,
			modal,
		},
		data () {
			return {
				store: store,
				loading: true,
				//token: 'QHyTosat3st1hTca9MII4ZT8zAAfEmCSRkE7JpRFN8vXz2YcUFKbOnvr2ItzKihjBqSo2L+St2o2awCJuR9ZYhBF2zmhZTq02wUDV1JrlPtJdI9zEGBYHtlPEza+Yjrg96ldnJHNx560asXkXKIEpQdB04t89/1O/w1cDnyilFU=',
				//client_secret: 'f5ba1cafa7a7057e68360d4d260827f6',
				//client_id: '1655871760',
				usernameInput: '',
				passwordInput: '',
				showPassword: false,
			}
		},
		async mounted () {
			this.loading = false
			functions.focusCursor('username')
		},
		methods: {
			t (w) { return translations.t(w) },
			async login () {
				await apiFunctions.login(this.usernameInput, this.passwordInput)
				this.$router.push({ name: 'home' })
			},
			//goToPage2 () {
			//	this.$router.push({ name: 'pageTwo', params: { thruParams: 'this was sent from the login page' } })
			//},
		} // methods
	} // export
</script>
<style scoped>
</style>
