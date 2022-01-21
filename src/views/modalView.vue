<template>
	<div>
		<event v-if="page === 'event'"
				:key="page + 'event'"/>
		<login-register v-show="page === 'loginRegister'" :tryLine="page === 'loginRegister'"
				:key="page + 'loginRegister'"/>
		<register-with-email v-show="page === 'registerWithEmail'"
				:key="page + 'registerWithEmail'"/>
		<add-event v-show="page === 'addEvent'"
				:key="page + 'addEvent'"/>
		<settings v-show="page === 'settings'" :tryLine="page === 'settings'"
				:key="page + 'settings'"/>
		<forgot-password v-show="page === 'forgotPassword'"
				:key="page + 'forgotPassword'"/>
		<reset-password v-show="page === 'resetPassword'"
				:key="page + 'resetPassword'"/>
		<about-us v-show="page === 'aboutUs'"
				:key="page + 'aboutUs'"/>
		<faq v-show="page === 'faq'"
				:key="page + 'faq'"/>
		<experiment1 v-show="page === 'experiment1'"
				:key="page + 'experiment1'"/>
		<experiment2 v-show="page === 'experiment2'"
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
	import resetPassword from '@/views/resetPassword'
	import forgotPassword from '@/views/forgotPassword'
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
			resetPassword,
			forgotPassword,
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
		computed: {
			page () {
				if (f.currentPage) {
					return f.currentPage.page
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