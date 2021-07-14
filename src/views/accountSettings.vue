<template>
	<div>
		<div v-if="!loading">
			<menus-header @logoutLoading="loading=true"/>
			<div class="box">
				<div>
					<h1>{{ t('SETTINGS') }}</h1>
				</div>
				<div class="dual-set">
					<div>
						<button class="no-border-button" v-on:click.prevent="store.user.do_get_emails=!store.user.do_get_emails">
							<div style="font-size: 18px;">{{ t('GET EMAILS') }}&nbsp;</div>
						</button>
					</div>
					<div>
						<input type="checkbox" class="checkbox" v-model="store.user.do_get_emails"/>
					</div>
				</div>
				<!--div>
					<h2>{{ t('CHANGE PASSWORD') }}</h2>
				</div-->
			</div>
			<!--a href="https://lin.ee/UeSvNxR"><img height="36" border="0" src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png"></a-->
		</div>
		<div class="loading" v-else></div>
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
		name: 'accountSettings',
		components: {
			menusHeader,
			modal,
		},
		data () {
			return {
				store: store,
				loading: true,
			}
		},
		watch: {
			async 'store.user.do_get_emails' () {
				await apiFunctions.updateUserDoGetEmails()
			},
		},
		async mounted () {
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
.dual-set {
	height: 24px;
	display: flex;
	flex-direction: row;
	align-items: flex-end;
	padding: 0;
}
.checkbox {
	height: 20px;
	width: 20px;
}
</style>
