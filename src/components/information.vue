<template>
	<modal @closeModals="closeInfo">
		<div slot="contents" class="modal">
			<div style="align-self: flex-end; padding-bottom: 5px;">
				<button v-on:click.prevent="closeInfo" class="no-border-button x-button">
					✖
				</button>
			</div>
			<div style="white-space: pre-line;">
				{{ theInfo[whichInfo] }}<br>
				For more info, go here [link]
			</div>
		</div>
	</modal>
</template>
<script>
	import modal from '@/components/modal'
	export default {
		name: 'information',
		components: {
			modal,
		},
		props: {
			closeInfo: {},
			whichInfo: {},
		},
		data () {
			return {
				theInfo: {
					'events': 'Upcoming events can be displayed by location, calendar, or list format. Click into an event to find more information. \n\nMap key: \n Past events \n Upcoming private events \n Upcoming public events',
					'peopleFilters': 'All: Public events + events to which you have and have not been invited. \n \nMine: Events to which you have been invited/have confirmed attendance. \n\nPeople I follow: Feature currently under construction',
				}
			}
		},
		mounted () {
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>