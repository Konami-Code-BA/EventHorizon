<template>
	<div>
		<event v-if="page === 'event'"/>
		<login-register v-show="page === 'loginRegister'"
				:key="page + 'loginRegister'"
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"/>
		<register-with-email v-show="page === 'registerWithEmail'"
				:key="page + 'registerWithEmail'"
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"/>
		<add-event v-show="page === 'addEvent'"
				:key="page + 'addEvent'"
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"/>
		<settings v-show="page === 'settings'"
				:key="page + 'settings'"
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"/>
		<aboutUs v-show="page === 'aboutUs'"
				:key="page + 'aboutUs'"
				@startLoading="$emit('startLoading')"
				@endLoading="$emit('endLoading')"/>
	</div>
</template>
<script>
	import store from '@/store'
	import event from '@/views/event'
	import loginRegister from '@/views/loginRegister'
	import registerWithEmail from '@/views/registerWithEmail'
	import addEvent from '@/views/addEvent'
	import settings from '@/views/settings'
	import aboutUs from '@/views/aboutUs'
	import f from '@/functions/functions.js'
	export default {
		name: 'modalView',
		components: {
			event,
			loginRegister,
			registerWithEmail,
			addEvent,
			settings,
			aboutUs,
		},
		data () {
			return {
				store: store,
				//page: null,
			}
		},
		computed: {
			page () {
				console.log('here', f.currentPage.page)
				if (f.currentPage) {
					return f.currentPage.page
				}
			},
		},
		//watch: {
		//	'store.pages' () {
		//		console.log('did this happen?', f.currentPage.page)
		//		this.page = f.currentPage.page
		//	},
		//},
		mounted () {
			this.$emit('endLoading')
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>