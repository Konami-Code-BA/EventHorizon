<template>
	<div>
		<div class="main">
			<div style="font-size: 36px;">{{ t('ADD EVENT') }}</div>
			<div class="line-height"></div>
			<div style="display: flex; flex-direction: column; align-items: center;">
				<button class="button" v-on:click.prevent="createEvent()" :disabled="!isAdmin">
					<div style="font-size: 18px;">{{ t('ADD') }}</div>
				</button>
				<div style="color: grey" v-if="!isAdmin"><small>({{ t('COMING SOON') }})</small></div>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'addEvent',
		components: {
			modal,
		},
		data () {
			return {
				store: store,
				showAddEventModal: false,
			}
		},
		computed: {
			isAdmin () {
				return functions.isAdmin
			},
		},
		watch: {
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async createEvent () {
				await apiFunctions.createEvent({  // lets make this a form
					name: 'name',
					description: 'description',
					address: '〒160-0023 東京都新宿区西新宿３丁目２−9',
					venue_name: 'venue_name',
					date_time: new Date('2021-12-31T03:24:00'),
					include_time: true,
					is_private: true,
					hosts: [],
					invited: [],
					confirmed_guests: [],
					interested: [],
				})
			}
		} // methods
	} // export
</script>
<style scoped>
</style>
