<template>
	<div>
		<div v-if="!loading">
			<menus-header/>
			<div class="box">
				<h1 style="text-align: center">EVENT HORIZON</h1>
				<div class="container">
					<img src="../assets/pexels-photo-event1.jpg" class="wide-img">
					<h2 class="contained" style="background-color: #94877f;">FIND EVENTS. HAVE FUN.</h2>
				</div>
				<div class="container">
					<img src="../assets/pexels-photo-event2.jpeg" class="wide-img">
					<h2 class="contained" style="background-color: #574944;">MEET PEOPLE. NETWORK.</h2>
				</div>
				<div class="container">
					<img src="../assets/pexels-photo-event4.jpeg" class="wide-img">
					<h2 class="contained" style="background-color: #4e1713;">Hello</h2>
				</div>
				<button v-on:click.prevent="$router.push(name='loginRegister')" class="box-item" v-if="!isAuthenticatedUser">
					{{ t('NEW USER REGISTRATION') }}
				</button>
				<button v-on:click.prevent="$router.push(name='home')" class="box-item" v-else>
					{{ t('HOME') }}
				</button>
			</div>
		</div>
		<div class="loading" v-else></div>
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
