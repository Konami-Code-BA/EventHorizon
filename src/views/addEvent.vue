<template>
	<div>
		<div class="main">
			<div>
				<h1>ADD</h1>
			</div>
			<div>
				<button class="no-border-button" v-on:click.prevent="showCreateEventModal=true">
					<div style="font-size: 18px;">{{ t('CREATE EVENT') }}</div>
				</button>
			</div>
		</div>
		<modal v-show="showCreateEventModal" @closeModals="showCreateEventModal=false">
			<div slot="contents" class="createEventModal">
				<div style="align-self: flex-end">
					<button v-on:click.prevent="showCreateEventModal=false" class="no-border-button">
						✖
					</button>
				</div>
				<create-event @startLoading="$emit('endLoading')" @endLoading="$emit('endLoading')"/>
			</div>
		</modal>
	</div>
</template>
<script>
	import store from '@/store.js'
	import appHeader from '@/components/appHeader.vue'
	import createEvent from '@/components/createEvent.vue'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'addEvent',
		components: {
			appHeader,
			modal,
			createEvent,
		},
		data () {
			return {
				store: store,
				showCreateEventModal: false,
			}
		},
		watch: {
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
	.createEventModal {
		width: 85%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		background-color: #0b0015;
		border: 1px solid #5300e1;
		border-radius: 15px;
		padding: 20px;
		max-height: 80%;
		width: 85%;
		max-width: 300px;
		z-index: 101;
		pointer-events: auto;
	}
</style>
