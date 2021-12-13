<template>
	<div class="main">
		<div style="width: 100%; display: flex; flex-direction: row; align-items: center; justify-content: space-between">
			<div style="width: 16px"></div>
			<h1>Event</h1>
			<button v-on:click.prevent="$emit('closeModals')" class="no-border-button">
				✖
			</button>
		</div>
		<div class="flex-table">
			<div style="align-self: flex-end">
				<small>{{event['is_private'] ? 'PRIVATE EVENT' : 'PUBLIC EVENT'}}</small>
			</div>
			<div class="flex-row">
				<div>
					EVENT NAME:
				</div>
				<div>
					{{event['name']}}
				</div>
			</div>
			<div>
				DESCRIPTION:
			</div>
			<div style="align-self: center">
				{{event['description']}}
			</div>
			<div>
				VENUE:
			</div>
			<div style="align-self: center">
				{{event['venue_name']}}
			</div>
			<div class="flex-row">
				<div>
					ADDRESS:
				</div>
				<button v-on:click.prevent="$emit('goToMap')" class="no-border-button">
					See in map
				</button>
			</div>
			<div style="align-self: center">
				{{event['address']}}
			</div>
			<div class="flex-row">
				<div>
					DATE:
				</div>
				<div>
					{{event['date_time']}}
				</div>
			</div>
			<div class="flex-row">
			</div>
			<div class="flex-row">
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import appHeader from '@/components/appHeader.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'event',
		components: {
			appHeader,
			modal,
		},
		data () {
			return {
				store: store,
				event: {},
				eventId: null,
			}
		},
		props: {
			id: {},
		},
		async mounted () {
			if (this.$route.params.id) {
				this.eventId = this.$route.params.id
			} else {
				this.eventId = this.id
			}
			this.event = await apiFunctions.getEvent(this.eventId)
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
.flex-table {
	width: 100%;
	display: flex;
	flex-direction: column;
}
.flex-row {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}
</style>
