<template>
	<div>
		<div class="footer" style="width: 100%">
			<tabs :num-tabs="6" :initial="selectedTab" :key="selectedTab" @on-click="(arg) => { changeTab(arg) }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1">
					<img src="../assets/mapIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="2">
					<img src="../assets/profileIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="3">
					<img src="../assets/peopleIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="4">
					<img src="../assets/searchIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="5">
					<img src="../assets/plusIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="6">
					<img src="../assets/gearIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
			</tabs>
		</div>
	</div>
</template>
<script>
	import store from '@/store'
	import tabs from '@/components/tabs.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'appFooter',
		data () {
			return {
				store: store,
				languageMenu: false,
				pages: {
					'events': 1,
					'profile': 2,
					'people': 3,
					'search': 4,
					'addEvent': 5,
					'settings': 6,
				},
				selectedTab: 1,
			}
		},
		components: {
			tabs,
		},
		props: {
		},
		computed: {
		},
		mounted () {
		},
		watch: {
			'$route' () {
				this.selectedTab = this.pages[this.$route.name]
			}
		},
		methods: {
			t (w) { return translations.t(w) },
			changeTab (selectedTab) {
				this.selectedTab = selectedTab
				if (this.selectedTab === 1) {
					this.goToEvents()
				} else if (this.selectedTab === 2) {
					this.goToProfile()
				} else if (this.selectedTab === 3) {
					this.goToPeople()
				} else if (this.selectedTab === 4) {
					this.goToSearch()
				} else if (this.selectedTab === 5) {
					this.goToAddEvent()
				} else if (this.selectedTab === 6) {
					this.goToSettings()
				}
			},
			goToEvents () {
				if (this.$route.name != 'events') {
					this.$router.push({ name: 'events' })
				}
			},
			goToProfile () {
				if (this.$route.name != 'profile') {
					this.$router.push({ name: 'profile' })
				}
			},
			goToPeople () {
				if (this.$route.name != 'people') {
					this.$router.push({ name: 'people' })
				}
			},
			goToSearch () {
				if (this.$route.name != 'search') {
					this.$router.push({ name: 'search' })
				}
			},
			goToAddEvent () {
				if (this.$route.name != 'addEvent') {
					this.$router.push({ name: 'addEvent' })
				}
			},
			goToSettings () {
				if (this.$route.name != 'settings') {
					this.$router.push({ name: 'settings' })
				}
			},
		}
	}
</script>
<style scoped>
</style>