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
			<div v-for="item in list">
				{{ item.name }}
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import tabs from '@/components/tabs.vue'
	export default {
		name: 'profile',
		components: {
			tabs,
		},
		watch: {
			'selectedTab' () {
				if (this.selectedTab == 1) {
					this.list = this.guest
				} else {
					this.list = this.hosting
				}
			},
		},
		data () {
			return {
				store: store,
				selectedTab: 1,
				hosting: [],
				guest: [],
				list: [],
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
				let allEvents = await apiFunctions.getMyEvents()
				for (let i = 0; i < allEvents.length; i++) {
					if (Array.isArray(allEvents[i]['hosts']) && allEvents[i]['hosts'].includes(this.store.user.id)) {
						this.hosting.push(allEvents[i])
					} else {
						this.guest.push(allEvents[i])
					}
				}
				this.list = this.guest
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
</style>
