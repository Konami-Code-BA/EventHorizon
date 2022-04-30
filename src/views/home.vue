<template>
	<div>
		<div class="main">
			<div class="card-shape" style="height: calc(100% - 20px); width: 95%; margin-top: 10px; margin-bottom: 15px;">
				<div class="tabsdiv" style="width: 100%; display: flex; flex-direction: column; border-top: none; border-top-radius: 7px;">
					<div style="display: flex; flex-direction: row; align-items: center; justify-content: center; padding: 5px; position:relative;">
						<div>
							{{ t('EVENTS') }}
						</div>
						<div style="position: absolute; right: 0;">
							<button style="background: none; border: none"
									v-on:click.prevent="showInformation = 'events'">
								<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="events-info"/>
							</button>
						</div>
					</div>
					<tabs :num-tabs="3" :initial="selectedTab" :key="selectedTab"
							@on-click="(arg) => { selectedTab = arg }"
							style="border-left: none; border-right: none; border-bottom: none; height: auto !important;">
						<div slot="1" class="tab">
							<img src="@/assets/mapIcon.png" class="icon" style="vertical-align: bottom;"/>
						</div>
						<div slot="2" class="tab">
							<img src="@/assets/threeBarsHIcon.png" class="icon" style="vertical-align: bottom;"/>
						</div>
						<div slot="3" class="tab">
							<img src="@/assets/calendarIcon.png" class="icon" style="vertical-align: bottom;"/>
						</div>
					</tabs>
				</div>
				<events-map class="viewer events" v-show="selectedTab==1"
						:key="createComponentKey('map')"/>
				<events-list class="viewer events" v-show="selectedTab==2"
						:key="createComponentKey('list')"/>
				<events-calendar class="viewer events" v-show="selectedTab==3"
						:key="createComponentKey('cal')"/>
				<div class="tabsdiv" style="width: 100%; display: flex; flex-direction: column; border-bottom-left-radius: 7px; border-bottom-right-radius: 7px; border-bottom: none;">
					<tabs :num-tabs="3" :initial="1" @on-click="(arg) => { filterChange(arg) }" ref="filterTabs"
							style="border-left: none; border-right: none; border-bottom: none; height: auto !important;
							border-top: none;">
						<div slot="1" class="tab">
							<img src="@/assets/globeIcon.png" class="icon" style="vertical-align: bottom;"/>
						</div>
						<div slot="2" class="tab">
							<img src="@/assets/profileIcon.png" class="icon" style="vertical-align: bottom;"
									v-if="false"/>
							<img src="@/assets/greyProfileIcon.png" class="icon" style="vertical-align: bottom;"
									v-else/>
						</div>
						<div slot="3" class="tab">
							<img src="@/assets/greyPeopleIcon.png" class="icon" style="vertical-align: bottom;"/>
						</div>
					</tabs>
				</div>
			</div>
		</div>
		<information v-if="showInformation" :closeInfo="() => {showInformation=null}" :whichInfo="showInformation"/>
    	<flash-modal :text="t('COMING SOON')" ref="flashComingSoon" :time="1500"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import information from '@/components/information'
	import tabs from '@/components/tabs.vue'
	import eventsMap from '@/components/eventsMap.vue'
	import eventsCalendar from '@/components/eventsCalendar.vue'
	import eventsList from '@/components/eventsList.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import flashModal from '@/components/flashModal.vue'
	export default {
		name: 'home',
		components: {
			information,
			tabs,
			eventsMap,
			eventsCalendar,
			eventsList,
			flashModal,
		},
		data () {
			return {
				store: store,
				selectedTab: 1,
				hideTop: false,
				showPeopleInfo: false,
				showInformation: null,
			}
		},
		computed : {
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
		},
		async created () {
			// get query
			let params = this.$route.params
			let keys = Object.keys(params)
			if (keys.length === 0) {
				f.goToPage({ page: 'home', args: {} }) // this will push the given parameters as the initial page info
			} else if (keys.length === 1) {
				f.goToPage({ page: params.page, args: {} })
			} else {
				let page = params.page
				delete params.page
				f.goToPage({ page: page, args: params })
			}
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToMap () {  // what do i do with this
				this.closeEventModal()
				this.selectedTab = 1
			},
			createComponentKey(letters) {
				let key = JSON.stringify(this.store.events.display) + JSON.stringify(this.store.events.selected) + letters
				return key
			},
			async filterChange (selectedFilter) {
				if (!this.isAuthenticatedUser && selectedFilter === 2) {
					this.$refs.filterTabs.selected = 1
					f.goToPage({ page: 'loginRegister', args: {} })
					return
				} else if (selectedFilter === 3 || selectedFilter === 2) {
					this.$refs.filterTabs.selected = 1
					await this.$refs.flashComingSoon.flashModal()
					return
				}
				this.store.events.display = this.store.events[
					{ 1: 'all', 2: 'mine', 3: 'allPeople' }[selectedFilter]
				]
			},
		} // methods
	} // export
</script>
<style scoped>
	.viewer {
		width: 100%;
		height: 100%;
		overflow-x: hidden;
		overflow-y: hidden;
	}
	.tabsdiv {
		background-color: rgba(0, 0, 0, .2);
		border: 2px solid rgba(255, 255, 255, .3);
		border-left: none;
		border-right: none;
	}
	.tabs {
		justify-content: space-around;
	}
	.tab {
		width: 80px !important;
		height: 20px !important;
		min-width: 100% !important;
	}
	.events {
		border-top: none;
		border-bottom: none;
		border-radius: 0;
	}
	.selected {
		background-color: rgba(255, 255, 255, .2);  /*140,128,151,0.6 after combinging with #18002e*/
		width: 100%;
	}
	.filter-button {
		border: none;
		border-radius: 0;
		height: 20px;
		padding: 10px;
		padding-left: 35px;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: center;
		width: 100%;
		z-index: 2;
	}
	/*.dual-set {
		display: flex;
		flex-direction: row;
		align-self: center;
		align-items: center;
		justify-content: center;
		padding: 0;
		width: 100%;
	}*/
	.checkbox {
		position: fixed;
		height: 15px;
		width: 20px;
		z-index: 1;
		flex-shrink: 0;
	}
	.filters {
		display: flex;
		flex-direction: row;
		width: 100%;
		align-items: flex-start;
	}
</style>
