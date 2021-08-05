<template>
	<div>
		<div class="main">
			<div>
				<img src="../assets/eventhorizon.png" style="max-width: 300px; z-index: 1;">
			</div>
			<div style="text-align: center; font-size: 32px;">EVENT HORIZON</div>
			<div class="line-height"/>
			<div style="text-align: center; font-size: 24px; white-space: pre-line">{{ t('REACH OUT TO NEW HORIZONS') }}</div>
			<div class="line-height"/>
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
				<button v-on:click.prevent="$router.push({ name: 'loginRegister' })" class="button" v-if="!isAuthenticatedUser">
					{{ t('LOGIN / REGISTER') }}
				</button>
				<button v-on:click.prevent="$router.push({ name: 'guestHome' })" class="button" v-else>
					{{ t('HOME') }}
				</button>
		</div>
		<transition name="fade">
			<modal v-show="showCookiesModal" @closeModals="closeCookiesModal()">
				<div slot="contents" class="cookiesModal">
					<div style="align-self: flex-end">
						<button v-on:click.prevent="closeCookiesModal()" class="no-border-button">
							✖
						</button>
					</div>
					<div style="white-space: pre-line; text-align: center; font-weight: 400;">
						{{t('This site uses cookies')}}
					</div><br>
					<div style="text-align: center">
						<button v-on:click.prevent="closeCookiesModal()" class="button" style="width: 100%">
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
	import appHeader from '@/components/appHeader.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import modal from '@/components/modal'
	export default {
		name: 'front',
		components: {
			appHeader,
			modal,
		},
		computed: {
			isAuthenticatedUser () { return [1, 2].includes(store.user.groups[0]) },
		},
		data () {
			return {
				store: store,
				showCookiesModal: store.user.alerts.includes(1),
			}
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async closeCookiesModal () {
				this.showCookiesModal = false
				await apiFunctions.updateUserAlerts('Show Cookies')
			},
		}
	}
</script>
<style scoped>
	.cookiesModal {
		position: fixed;
		display: flex;
		flex-direction: column;
		z-index: 10000;
		background-color: #18002e;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		width: 50%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, 0);
	}
</style>
