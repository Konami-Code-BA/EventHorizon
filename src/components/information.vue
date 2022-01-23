<template>
	<modal @closeModals="closeInfo">
		<div slot="contents" class="modal">
			<div style="align-self: flex-end; padding-bottom: 5px;">
				<button v-on:click.prevent="closeInfo" class="no-border-button x-button">
					✖
				</button>
			</div>

<!--START INFO-->

			<!--peopleFilters-->
			<div v-if="whichInfo === 'peopleFilters'">
				{{'All: Public events + events to which you have and have not been invited. \n \nMine: Events to which you have been invited/have confirmed attendance. \n\nPeople I follow: Feature currently under construction'}}
			</div>
			
			<!--events-->
			<div v-if="whichInfo === 'events'">
				<div style="display: flex; flex-direction: row; justify-content: space-between;
						align-items: flex-start; height: 300px;">
					<div style="display: flex; flex-direction: column; justify-content: space-between;
							align-items: flex-start; height: 100%;">
						<div style="display: flex; flex-direction: column; justify-content: space-between;
								align-items: flex-start;">
							<div style="font-size: 25px;">
								INVITED
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center;">
								<img src="@/../dist/static/myMapIcon.png" style="width: 25px; height: 25px;"/>
								UPCOMING
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%">
								<img src="@/../dist/static/myPastMapIcon.png" style="width: 25px; height: 25px;"/>
								PAST
							</div>
						</div>
						<div style="display: flex; flex-direction: column; justify-content: space-between;
								align-items: flex-start">
							<div style="font-size: 25px;">
								PUBLIC
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center;">
								<img src="@/../dist/static/publicMapIcon.png" style="width: 25px; height: 25px;"/>
								UPCOMING
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%">
								<img src="@/../dist/static/publicPastMapIcon.png" style="width: 25px; height: 25px;"/>
								PAST
							</div>
						</div>
						<div style="display: flex; flex-direction: column; justify-content: space-between;
								align-items: flex-start">
							<div style="font-size: 25px;">
								PRIVATE
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center;">
								<img src="@/../dist/static/privateMapIcon.png" style="width: 25px; height: 25px;"/>
								UPCOMING
							</div>
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%">
								<img src="@/../dist/static/privatePastMapIcon.png" style="width: 25px; height: 25px;"/>
								PAST
							</div>
						</div>
					</div>
					<div style="width: 50%; white-space: pre-line;">
						{{'Upcoming events can be displayed by location, calendar, or list format. Click into an event to find more information.\n\nPrivate events\' locations aren\'t shown in the exact place.'}}
					</div>
				</div>
			</div>

<!--FINISH INFO-->

			<div class="line-height"/>
			
			<div style="display: flex; flex-direction: row;">
				For more info, go to the
				<button v-on:click.prevent="goToFaq()" class="link-button">
					FAQ
				</button>
			</div>
		</div>
	</modal>
</template>
<script>
	import modal from '@/components/modal'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
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
			}
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
			goToFaq () {
				f.goToPage({ page: 'faq', args: {} })
			},
		}
	}
</script>
<style scoped>
</style>