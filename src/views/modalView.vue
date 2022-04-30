<template>
	<div>
		<event v-if="page === 'event'"
				:key="page + 'event'"/>
		<login-register v-show="page === 'loginRegister'"
				:key="page + 'loginRegister'"/>
		<add-event v-show="page === 'addEvent'"
				:key="page + 'addEvent'"/>
		<settings v-show="page === 'settings'"
				:key="page + 'settings'"/>
		<welcome v-if="page === 'welcome'"
				:key="page + 'welcome'"
				@closeLanguage="$emit('closeLanguage')"/>
		<about-us v-show="page === 'aboutUs'"
				:key="page + 'aboutUs'"/>
		<faq v-show="page === 'faq'"
				:key="page + 'faq' + store.user.language"/>
		<experiment1 v-show="page === 'experiment1' && store.user.is_superuser"
				:key="page + 'experiment1'"/>
		<experiment2 v-show="page === 'experiment2' && store.user.is_superuser"
				:key="page + 'experiment2'"/>
		<!-- COMMENT THIS OUT BEFORE PUSHING TO PRODUCTION -->
	</div>
</template>
<script>
	import store from '@/store'
	import event from '@/views/event'
	import loginRegister from '@/views/loginRegister'
	import registerWithEmail from '@/views/registerWithEmail'
	import addEvent from '@/views/addEvent'
	import settings from '@/views/settings'
	import welcome from '@/views/welcome'
	import aboutUs from '@/views/aboutUs'
	import faq from '@/views/faq'
	import experiment1 from '@/views/experiment1'
	import experiment2 from '@/views/experiment2'
	import f from '@/functions/functions.js'
	export default {
		name: 'modalView',
		components: {
			event,
			loginRegister,
			registerWithEmail,
			addEvent,
			settings,
			welcome,
			aboutUs,
			faq,
			experiment1,
			experiment2,
		},
		data () {
			return {
				store: store,
				//page: null,
			}
		},
		props: {
		},
		computed: {
			page () {
				if (f.currentPage) {
					if (
						(f.isAuthenticatedUser && (
							f.currentPage.page === 'loginRegister' || f.currentPage.page === 'registerWithEmail'
						)) ||
						(!f.isAuthenticatedUser && f.currentPage.page === 'settings')
					) {
						f.goToPage({ page: 'home', args: {} })
						return
					} else {
						return f.currentPage.page
					}
				}
			},
		},
		mounted () {
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>