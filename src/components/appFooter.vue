<template>
	<div>
		<div class="footer" style="width: 100%">
			<tabs :num-tabs="6" :initial="selectedTab" :key="selectedTab" @on-click="(arg) => { changeTab(arg) }"
					style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1">
					<img src="@/assets/mapIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="2">
					<img src="@/assets/profileIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="3">
					<img src="@/assets/peopleIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="4">
					<img src="@/assets/searchIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="5">
					<img src="@/assets/plusIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="6">
					<img src="@/assets/gearIcon.png" class="icon" style="margin-bottom: 1px;"/>
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
				selectedTab: 0,
				pages: ['events', 'profile', 'people', 'search', 'addEvent', 'settings'],
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
				let ind = this.pages.indexOf(this.$route.name)
				if (ind != -1) {
					this.selectedTab = ind + 1
				} else {
					this.selectedTab = 0
				}
			},
		},
		methods: {
			t (w) { return translations.t(w) },
			changeTab (selectedTab) {
				let routes = ''
				if (selectedTab === 1) {
					this.selectedTab = selectedTab
				} else {
					this.selectedTab = 0
					routes += 'loginRegister'
				}
				for (let i = 0; i < this.pages.length; i++) {
					if (selectedTab === i+1 && !(routes+this.pages[i]).includes(this.$route.name)) {
						this.$router.push({ name: this.pages[i] }).catch(() => {})
					}
				}
			},
		}
	}
</script>
<style scoped>
	.tabs {
		border-bottom: none !important;
		border-left: none !important;
		border-right: none !important;
	}
</style>