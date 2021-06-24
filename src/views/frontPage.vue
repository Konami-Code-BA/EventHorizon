<template>
  <div>
		<menus-header/>
		<div class="box">
			<button v-on:click.prevent="$router.push(name='registration')" class="box-item" v-if="!isAuthenticatedUser">
				{{ t('REGISTER') }}
			</button>
			<button v-on:click.prevent="$router.push(name='home')" class="box-item" v-else>
				{{ t('HOME') }}
			</button>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'frontPage',
		components: {
			menusHeader,
		},
		computed: {
			isAuthenticatedUser () { return Boolean(store.user.username) },
		},
		data () {
			return {
				store: store,
				loading: true,
			}
		},
		async mounted () {
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
		}
	}
</script>
<style scoped>
</style>
