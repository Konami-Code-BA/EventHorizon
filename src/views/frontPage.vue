<template>
	<div>
		<div v-if="!loading">
			<menus-header @logoutLoading="loading=true"/>
			<div class="box">
				<div style="text-align: center; font-size: 32px;">EVENT HORIZON</div>
				<div class="box-height"></div>
				<div style="text-align: center; font-size: 24px; white-space: pre-line">{{ t('EXPAND YOUR REACH TO NEW HORIZONS') }}</div>
				<div class="box-height"></div>
				<!--div class="container">
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
				</div-->
				<button v-on:click.prevent="loading=true; $router.push(name='loginRegister')" class="box-item" v-if="!isAuthenticatedUser">
					{{ t('LOGIN / REGISTER') }}
				</button>
				<button v-on:click.prevent="loading=true; $router.push(name='home')" class="box-item" v-else>
					{{ t('HOME') }}
				</button>
			</div>
		</div>
		<div class="loading" v-else></div>
		<transition name="fade">
			<modal v-show="showCookiesModal" @closeModals="closeCookiesModal()"
				id="showCookiesModal">
				<div slot="contents" class="showCookiesModal">
					<div style="white-space: pre-line; text-align: center; font-weight: 400;">
						{{t('This site uses cookies')}}
					</div><br>
					<div style="text-align: center">
						<button v-on:click.prevent="closeCookiesModal()">
							<big>{{t('OK')}}</big>
						</button>
					</div><br><br>
				</div>
			</modal>
		</transition>
	</div>
</template>
<script>
	import store from '@/store.js'
	import menusHeader from '@/components/menusHeader.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import modal from '@/components/modal'
	export default {
		name: 'frontPage',
		components: {
			menusHeader,
			modal,
		},
		computed: {
			isAuthenticatedUser () { return store.user.groups.includes(1) || store.user.groups.includes(2) },
		},
		data () {
			return {
				store: store,
				loading: true,
				showCookiesModal: store.user.alerts.includes(1),
			}
		},
		async mounted () {
			this.loading = false
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				console.log('store.user', store.user)
				await apiFunctions.updateUserAlerts('Show Cookies')
			},
		}
	}
</script>
<style scoped>
	.showCookiesModal {
		position: fixed;
		z-index: 10000;
		background-color: #00022e;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, 0);
	}
</style>
