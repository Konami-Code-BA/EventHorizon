<template>
	<div class="main">
		<div style="font-size: 36px">{{ store.user.display_name }}</div>
		<div class="line-height"></div>
		<div style="width: 100%;">
			<tabs :num-tabs="2" :initial="selectedTab" :key="selectedTab" @on-click="(arg) => { selectedTab = arg }"
					class="tabs">
				<div slot="1">
					GUEST
				</div>
				<div slot="2">
					HOSTING
				</div>
			</tabs>
		</div>
		<div class="viewer">
			<div class="list" v-if="list.length > 0">
				<div v-for="item in list">
					<button v-on:click.prevent="$emit('openEventModal', item.id)" class="no-border-button"
							style="text-align: left; white-space: nowrap">
						{{ item.date_time.split('T')[0] }}: {{ item.name }}
					</button>
				</div>
			</div>
			<div v-else>
				{{ t('NO EVENTS') }}
			</div>
		</div>
		<event v-if="showEventModal" @goToMap="goToMap()" :id="selectedEventId" @closeModals="closeEventModal()"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import tabs from '@/components/tabs.vue'
	import event from '@/components/event.vue'
	export default {
		name: 'profile',
		components: {
			tabs,
			event,
		},
		watch: {
			'selectedTab' () {
				if (this.selectedTab == 1) {
					this.list = this.guest
				} else {
					this.list = this.hosting
				}
				console.log(this.list.length)
			},
		},
		data () {
			return {
				store: store,
				selectedTab: 1,
				hosting: [],
				guest: [],
				list: [],
				sorted_events: [],
				selectedEventId: null,
				showEventModal: false,
			}
		},
		async mounted () {
			this.getMyEvents()
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async getMyEvents () {
				this.$emit('startLoading')
				let allEvents = await api.getMyEvents()
				for (let i = 0; i < allEvents.length; i++) {
					if (this.isHost(allEvents[i])) {
						this.hosting.push(allEvents[i])
					} else {
						this.guest.push(allEvents[i])
					}
				}
				this.guest = this.sortEventsByDate(this.guest)
				this.hosting = this.sortEventsByDate(this.hosting)
				this.list = this.guest
			},
			sortEventsByDate (events) {
				return f.sortEventsByDate(events)
			},
			openEventModal (id) {
				f.setBackButtonToCloseModal(this, window, this.closeEventModal)
				this.selectedEventId = id
				this.showEventModal = true
			},
			closeEventModal () {
				// after closing, it goes to the previously opened event in map. should it also scroll to previously
				// opened event in the list and calendar?
				f.freeUpBackButton(this)
				this.showEventModal = false
			},
			isHost (event) {
				return f.isHost(event)
			},
			goToMap () {
				1
			},
		} // methods
	} // export
</script>
<style scoped>
	.viewer {
		width: 100%;
		height: 100%;
		margin-bottom: 5px;
		border: 2px solid rgba(255, 255, 255, .1);
		border-bottom-left-radius: 7px;
		border-bottom-right-radius: 7px;
	}
	.tabs {
		background-color: rgba(0, 0, 0, .2);
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
		border-bottom: none !important;
	}
	.list {
		display: flex;
		flex-direction: column;
		overflow-y: scroll;
		overflow-x: hidden;
		align-items: flex-start;
	}
</style>
