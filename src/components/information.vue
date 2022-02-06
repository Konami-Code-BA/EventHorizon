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
				<p>{{t('ALL')}}{{`:\xa0\xa0\xa0\xa0`}}{{t('ALL EVENTS')}}</p>
				<p>{{t('MINE')}}{{`:\xa0\xa0\xa0\xa0`}}{{t('EVENTS I AM AFFILIATED WITH')}}</p>
				<p>{{t('PEOPLE I FOLLOW')}}{{`:\xa0\xa0\xa0\xa0`}}{{t('COMING SOON')}}</p>
			</div>
			
			<!--events-->
			<div v-if="whichInfo === 'events'" style="display: flex; flex-direction: column; align-items: center;">
				<h2 style="text-align: center">{{t('EVENT TYPES')}}</h2>
				<div style="display: flex; flex-direction: column; justify-content: space-between;
						align-items: center; height: 300px;">
					<div style="display: flex; flex-direction: column; justify-content: space-between;
							align-items: center; height: 100%;">
						<div style="display: flex; flex-direction: column;
								align-items: center;">
							<div style="font-size: 18px; border-bottom: solid 1px; width: 100%; text-align: center;">
								{{t('invited2')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/myMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('UPCOMING')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/myPastMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('PAST')}}
							</div>
						</div>
						<div style="display: flex; flex-direction: column;
								align-items: center">
							<div style="font-size: 18px; border-bottom: solid 1px; margin-top: 10px; width: 100%;
									text-align: center;">
								{{t('PUBLIC')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/publicMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('UPCOMING')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/publicPastMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('PAST')}}
							</div>
						</div>
						<div style="display: flex; flex-direction: column;
								align-items: center">
							<div style="font-size: 18px; border-bottom: solid 1px; margin-top: 10px; width: 100%;
									text-align: center;">
								{{t('PRIVATE')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/privateMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('UPCOMING')}}
							</div>
							<div style="display: flex; flex-direction: row;
									align-items: center;">
								<img src="@/assets/privatePastMapIcon.png" style="width: 25px; height: 25px;"/>
								{{t('PAST')}}
							</div>
						</div>
					</div>
					<div style="width: 100%; white-space: pre-line;">
						{{ t('Note: Private events\' locations aren\'t shown in the exact place.') }}
					</div>
				</div>
			</div>

			<!--FINISH INFO-->

			<div class="line-height"/>
			
			<div style="display: flex; flex-direction: row;">
				{{ t('For more info, go to the') }}
				<button v-on:click.prevent="goToFaq()" class="link-button">
					FAQ
				</button>
				{{ t('to') }}
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