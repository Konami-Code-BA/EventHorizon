<template>
	<div>
		<div class="footer" style="width: 100%;">
			<tabs :num-tabs="4" :initial="2" @on-click="selectedTab = $event" style="background-color: rgba(0, 0, 0, .5);">
				<div slot="1">
					<img src="../assets/homeIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="2">
					<img src="../assets/homeIcon.png" class="icon" style="margin-bottom: 2px;"/>
				</div>
				<div slot="3">
					<img src="../assets/profileIcon.png" class="icon" style="margin-bottom: 1px;"/>
				</div>
				<div slot="4">
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
				mainMenu: false,
				languageMenu: false,
			}
		},
		components: {
			tabs,
		},
		props: {
		},
		computed: {
		},
		async mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToHome () {
				if (this.$route.name !== 'home') {
					this.$router.push({ name: 'home' })
				} else {
					this.mainMenu = false
				}
			},
			goToFront () {
				if (this.$route.name !== 'front') {
					this.$router.push({ name: 'front' })
				}
			},
			goToLoginRegister () {
				if (this.$route.name !== 'loginRegister') {
					this.$router.push({ name: 'loginRegister' })
				}
			},
			goToSettings () {
				if (this.$route.name !== 'settings') {
					this.$router.push({ name: 'settings' })
				} else {
					this.mainMenu = false
				}
			},
		}
	}
</script>
<style scoped>
</style>