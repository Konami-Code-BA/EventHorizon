<template>
	<modal @closeModals="closeInfo" ref="information">
		<div slot="contents" class="modal" style="width: 100%;">
			<div style="overflow-y: hidden; padding-right: 0; padding-left: 10px; display: flex; flex-direction: column;
					width: 100%;">
				<x-close-button :closeFunc="() => {$refs.information.closeModals()}" style="align-self: flex-end;
						padding-right: 10px;"/>

				<div style="overflow-y: scroll; width: 100%; display: flex; flex-direction: column;
						justify-content: flex-start;">

					<!--events-->
					<div v-if="whichInfo === 'events'" style="display: flex; flex-direction: column;
							align-items: center; flex-shrink: 0; height: 100%;">
						<h2 style="text-align: center; font-size: 20px; margin: 0.4em;">{{t('EVENTS')}}</h2>
						<div style="display: flex; flex-direction: column; justify-content: space-between;
								align-items: center; height: 300px;">
							<div style="display: flex; flex-direction: column; justify-content: space-between;
									align-items: center; height: 100%;">
								<div style="display: flex; flex-direction: column;
										align-items: center; padding-top: 10px;">
									<div class="sub-title">
										{{t('invited2')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/upcomingMyMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('UPCOMING')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/pastMyMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('PAST')}}
									</div>
								</div>
								<div style="display: flex; flex-direction: column;
										align-items: center; padding-top: 10px;">
									<div class="sub-title">
										{{t('PUBLIC')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/upcomingPublicMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('UPCOMING')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/pastPublicMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('PAST')}}
									</div>
								</div>
								<div style="display: flex; flex-direction: column;
										align-items: center; padding-top: 10px;">
									<div class="sub-title">
										{{t('PRIVATE')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/upcomingPrivateMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('UPCOMING')}}
									</div>
									<div class="nav-items">
										<img src="@/assets/pastPrivateMapIcon2.png" style="width: 25px; height: 25px;"/>
										{{t('PAST')}}
									</div>
								</div>
							</div>

							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%; padding-top: 10px;">
								<div style="width: auto;">
									<img src="@/assets/globeIcon.png" class="icon" style="vertical-align: bottom;"/>
								</div>
								<div style="width: 80%;">
									{{ t('ALL EVENTS') }}
								</div>
							</div>

							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%; padding-top: 10px;">
								<div style="width: auto;">
									<img src="@/assets/profileIcon.png" class="icon" style="vertical-align: bottom;"/>
								</div>
								<div style="width: 80%;">
									{{ t('EVENTS I AM AFFILIATED WITH') }}
								</div>
							</div>
							
							<div style="display: flex; flex-direction: row; justify-content: space-between;
									align-items: center; width: 100%; padding-top: 10px;">
								<div style="width: auto;">
									<img src="@/assets/peopleIcon.png" class="icon" style="vertical-align: bottom;"/>
								</div>
								<div style="width: 80%;">
									{{ t('COMING SOON') }}
								</div>
							</div>
							<div style="width: 100%; white-space: pre-line; font-size:0.8em; margin-bottom: 0.5em;">
								{{ t('Note: Private events\' locations aren\'t shown in the exact place.') }}
							</div>
						</div>
					</div>

					<!--attendingStatus-->
					<div v-if="whichInfo === 'attendingStatus'" style="display: flex; flex-direction: column;
							justify-content: flex-start; align-items: center; width: 100%;">
						<h2 style="text-align: center; font-size: 20px; margin: 0.4em;">{{t('ATTENDING STATUS')}}</h2>
						<div style="display: flex; flex-direction: row; justify-content: space-between;
								align-items: center; width: 100%;">
							<div style="width: 30%;">
								{{t('I WILL ATTEND')}}
							</div>
							<div style="width: 60%;">
								{{t('I WILL ATTEND explanation')}}
							</div>
						</div>

						<div class="line-height"/>

						<div style="display: flex; flex-direction: row; justify-content: space-between;
								align-items: center; width: 100%;">
							<div style="width: 30%;">
								{{t('maybe')}}
							</div>
							<div style="width: 60%;">
								{{t('maybe explanation')}}
							</div>
						</div>

						<div class="line-height"/>
						
						<div style="display: flex; flex-direction: row; justify-content: space-between;
								align-items: center; width: 100%;">
							<div style="width: 30%;">
								{{t('wait_list')}}
							</div>
							<div style="width: 60%;">
								{{ t('wait_list explanation') }}
							</div>
						</div>

						<div class="line-height"/>
						
						<div style="display: flex; flex-direction: row; justify-content: space-between;
								align-items: center; width: 100%;">
							<div style="width: 30%;">
								{{t('invite_request')}}
							</div>
							<div style="width: 60%;">
								{{ t('invite_request explanation') }}
							</div>
						</div>

						<div class="line-height"/>
						
						<div style="display: flex; flex-direction: row; justify-content: space-between;
								align-items: center; width: 100%;">
							<div style="width: 30%;">
								{{t('decline')}}
							</div>
							<div style="width: 60%;">
								{{ t('decline explanation') }}
							</div>
						</div>
					</div>

				</div>

				<div style="display: flex; flex-direction: row; font-size:0.8em; flex-shrink: 0;
						height: auto; padding-top: 10px;">
					{{ t('For other info, go to the') }}
					<button v-on:click.prevent="$refs.information.closeModals(); goToFaq()" class="link-button">
						FAQ
					</button>
					{{ t('to') }}
				</div>
			</div>
		</div>
	</modal>
</template>
<script>
	import modal from '@/components/modal'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import xCloseButton from '@/components/xCloseButton.vue'
	export default {
		name: 'information',
		components: {
			modal,
			xCloseButton,
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

.sub-title {
  font-size: 16px;
  border-bottom: solid 1px;
  width: 100%;
  text-align: center;
}

.nav-items {
  display: flex;
  flex-direction: row;
  align-items: center;
  font-size: 0.8em;
}
</style>
