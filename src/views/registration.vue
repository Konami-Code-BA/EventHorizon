<template>
	<div>
		<div v-if="!loading">
			<div class="box">
				<menus-header :isRegistrationPage="true"/>
				<br>
				<form v-on:keyup.enter="register()">
					<input :placeholder="t('USERNAME')" v-model="usernameInput" type="text" ref="username"
						class="box-item" id="username"/><br>
					<br>
					<input :placeholder="t('EMAIL')" v-model="emailInput" type="email" class="box-item"/><br>
					<br>
					<div style="display: flex;">
						<input :placeholder="t('PASSWORD')" v-model="passwordInput"
							:type="[showPassword ? 'text' : 'password']" class="box-item" style="flex-grow: 1;"
							id="password"/>
						<button v-on:click.prevent="showPassword = !showPassword" class="box-item" style="width: 60px"
							id="show">
							<small v-if="!showPassword">{{ t('SHOW') }}</small>
							<small v-else>{{ t('HIDE') }}</small>
						</button><br>
					</div>
				</form>
				<br>
				<button v-on:click.prevent="register()" class="box-item">
					{{ t('REGISTER') }}
				</button><br>
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
	import modal from '@/components/modal.vue'
	import menusHeader from '@/components/menusHeader.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'registration',
		components: {
			modal,
			menusHeader,
		},
		data () {
			return {
				store: store,
				loading: true,
				usernameInput: '',
				emailInput: '',
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
			async register () {
				await apiFunctions.register(this.usernameInput, this.emailInput, this.passwordInput)
				this.$router.push({ name: 'home' })
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
