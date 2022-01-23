<template>
	<div>
		<div class="main" style="padding-top: 5px;">
			<div class="viewer filters" style="display: flex; flex-direction: column; align-items: center;
					width: 100%; min-height: 105px; height: 105px;"><!--remove filters from class and check mac is ok-->
				<div style="border-bottom: 2px solid rgba(255, 255, 255, .3); width: 100%; display: flex;
						flex-direction: row; align-items: center; justify-content: center; padding: 5px;">
					<div>
						{{ t('SELECT WHAT EVENTS TO DISPLAY') }}
					</div>
					<div style="position: absolute; right: 2%;">
						<button style="background: none; border: none"
								v-on:click.prevent="showInformation = 'peopleFilters'">
							<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="people-info"/>
						</button>
					</div>
				</div>
				<div style="display: flex; flex-direction: column; align-items: flex-start; width: 100%;
						padding-top: 5px; padding-bottom: 5px;">
					<div class="filters">
						<input type="checkbox" class="checkbox" v-model="filters['all']"
								@click="filterChange('all')"/>
						<button class="button filter-button" :class="{ selected : filters['all']}"
								v-on:click.prevent="filters['all']=!filters['all']; filterChange('all')">
							{{ t('ALL') }}
						</button>
					</div>
					<div class="filters">
						<input type="checkbox" class="checkbox" v-model="filters['mine']"
								@click="filterChange('mine')"/>
						<button class="button filter-button" :class="{ selected : filters['mine']}"
								v-on:click.prevent="filters['mine']=!filters['mine']; filterChange('mine')">
								{{ t('MINE') }}
						</button>
					</div>
					<div class="filters">
						<input type="checkbox" class="checkbox" v-model="filters['allPeople']"
								@click="filterChange('allPeople')"/>
						<button class="button filter-button" :class="{ selected : filters['allPeople']}" disabled
								v-on:click.prevent="filters['allPeople']=!filters['allPeople'];
								filterChange('allPeople')">
							<div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; width: 100%;">
								<div>
									{{ t('PEOPLE I FOLLOW') }}
								</div>
								<div>
									<small>({{ t('COMING SOON') }})</small>
								</div>
							</div>
						</button>
					</div>
				</div>
			</div>
			<div class="tabsdiv" style="width: 100%; display: flex; flex-direction: column;">
				<!--div style="position: fixed; margin-top: 15px; right: 2px; z-index: 10;">
					<button class="button" v-on:click.prevent="hideTop = !hideTop" style="border: 2px solid rgba(140, 128, 151, 0.6); border-radius: 7px; width: 25px; height: 25px; padding: 0; background-color: #18002e; padding-bottom: 1px;">
						<img src="@/assets/fullScreen.png" class="icon" style="width: 80%; height: 80%"/>
					</button>
				</div-->
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center; padding: 5px;">
					<div>
						{{ t('EVENTS') }}
					</div>
					<div style="position: absolute; right: 2%;">
						<button style="background: none; border: none"
								v-on:click.prevent="showInformation = 'events'">
							<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="events-info"/>
						</button>
					</div>
				</div>
				<tabs :num-tabs="3" :initial="selectedTab" :key="selectedTab"
						@on-click="(arg) => { selectedTab = arg }"
						style="border-left: none; border-right: none; border-bottom: none; height: auto !important;">
					<div slot="1">
						<img src="@/assets/mapIcon.png" class="icon"/>
					</div>
					<div slot="2">
						<img src="@/assets/threeBarsHIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
					<div slot="3">
						<img src="@/assets/calendarIcon.png" class="icon" style="vertical-align: bottom"/>
					</div>
				</tabs>
			</div>
			<events-map class="viewer events" v-show="selectedTab==1"
					:key="createComponentKey('map')"/>
			<events-list class="viewer events" v-show="selectedTab==2"
					:key="createComponentKey('list')"/>
			<events-calendar class="viewer events" v-show="selectedTab==3"
					:key="createComponentKey('cal')"/>
		</div>
		<information v-if="showInformation" :closeInfo="() => {showInformation=null}" :whichInfo="showInformation"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import information from '@/components/information'
	import tabs from '@/components/tabs.vue'
	import eventsMap from '@/components/eventsMap.vue'
	import eventsCalendar from '@/components/eventsCalendar.vue'
	import eventsList from '@/components/eventsList.vue'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'home',
		components: {
			modal,
			information,
			tabs,
			eventsMap,
			eventsCalendar,
			eventsList,
		},
		data () {
			return {
				store: store,
				selectedTab: 1,
				hideTop: false,
				filters: {'all': true, 'mine': false, 'allPeople': false},
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
				let key = (this.store.events.display.length > 0 ? this.store.events.display[0]['id'] : 0).toString()
				key += (this.store.events.selected ? this.store.events.selected.id : 0).toString() + letters
				return key
			},
			doFiltering () {
				this.store.events.display = []
				let keys = Object.keys(this.filters)
				for (let i = 0; i < keys.length; i++) {
					if (this.filters[keys[i]]) {  // if this filter is true
						this.store.events.display = this.store.events.display.concat(this.store.events[keys[i]])
					}
				}
				window.initMap()
			},
			filterChange (changed) {
				let keys = Object.keys(this.filters)
				if (changed === 'all') {  // if it was 'all' that changed
					if (this.filters[changed]) {  // if selected, deselect all others
						for (let i = 0; i < keys.length; i++) {
							if (keys[i] != changed) {
								this.filters[keys[i]] = false
							}
						}
					} else {  // if deselected, 'all' can only be deselected if its the only one selected, so
						this.filters['none'] = true  // make 'none' true
					}
				} else {  // if it was some other filter selection that changed
					if (this.filters[changed]) {  // if selected
						if (this.filters['all']) {  // deselect 'all' filter, if it is selected
							this.filters['all'] = false
						}
					} else {  // if deselected
						if (!Object.values(this.filters).includes(true)) {  // if no other filter is selected
							this.filters['none'] = true  // make 'none' true
						} // otherwise do nothing special, the changed filter has already been changed
					}
				}
				this.doFiltering()
			},
		} // methods
	} // export
</script>
<style scoped>
	.tabsdiv {
		background-color: rgba(0, 0, 0, .2);
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
		border: 2px solid rgba(255, 255, 255, .3);
	}
	.events {
		border-top: none;
		border-top-left-radius: 0;
		border-top-right-radius: 0;
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
	}
	.filters {
		display: flex;
		flex-direction: row;
		width: 100%;
		align-items: center;
	}
</style>
