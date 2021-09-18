<template>
	<div>
		<div class="main">
			<div>
				<h1>{{ t('SETTINGS') }}</h1>
			</div>
			<div>
				<button class="no-border-button" v-on:click.prevent="showCreateEventModal=true">
					<div style="font-size: 18px;">{{ t('CREATE EVENT') }}</div>
				</button>
			</div>
		</div>
		<modal v-show="showCreateEventModal" @closeModals="showCreateEventModal=false">
			<div slot="contents" class="createEventModal">
				<div style="text-align: right">
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
		position: fixed;
		z-index: 100;
		background-color: #18002e;
		border-radius: 15px;
		border: 1px solid #5300e1;
		padding: 20px;
		width: 85%;
		height: 100%;
		top: 50%;
		left: 50%;
		transform: translate(-50%, 0);
	}
</style>
