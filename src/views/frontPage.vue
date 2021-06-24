<template>
  <div>
		<menus-header/>
		<div class="box">
			<h1 style="text-align: center">EVENT HORIZON</h1>
			<button v-on:click.prevent="$router.push(name='registration')" class="box-item">{{ t('REGISTER') }}</button>
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
