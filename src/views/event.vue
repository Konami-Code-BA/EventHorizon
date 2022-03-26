<template>
	<div class="main" v-if="store.events.selected && event" style="overflow-y: scroll;">
		<div style="width: 100%; display: flex; flex-direction: column; align-items: center; height: auto;">
			<div class="flex-row" style="align-items: center; justify-content: center; height: 60px;">
				<div style="max-width: 100%; overflow-x: scroll; max-height: 100%; overflow-y: hidden;
						white-space: nowrap; font-size: 22px;">
					{{event.name}}
				</div>
			</div>
			<div class="flex-row" style="justify-content: space-between;">
				<div>
					{{ getDate }}
				</div>
				<div>
					<small>{{ event.is_private ? t('PRIVATE') : t('PUBLIC') }}</small>
				</div>
			</div>
			<img :src="image" style="
					width: 100%; height: auto; max-width: 500px; margin-top: 16px; margin-bottom: 10px;
			"/>
			<div class="flex-table" style="height: auto;">
				<small class="event-attr">{{t('ATTENDING STATUS')}}</small>
				<div v-show="!isSpaceToAttend" style="color: red; width: 100%; text-align: center; margin-bottom: 0.7em; margin-top: 4px;">
					{{ t('THE EVENT IS FULL') }}
				</div>
				<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%; overflow-x: hidden; margin-bottom: 0.7em; margin-top: 4px;">
					<div style="display: flex; flex-direciton: row; justify-content: center; align-items: center;
							width: 100%;">
						<div style="width: 35px; flex-shrink: 0"/>
						<div style="display: flex; flex-direction: column; align-items: center; width: calc(100% - 70px);">
							<div class="dual-set" v-if="myAttendingStatus['invited']"
									style="border-bottom: 2px solid rgba(255, 255, 255, .3); width: 80%;
									margin-bottom: 5px;">
								{{ t('invited') }}
								<input type="checkbox" class="checkbox" checked="checked" onclick="return false;"/>
							</div>
							<!--if invited, can click maybe / attending / decline-->
							<div v-if="myAttendingStatus['invited']" style="width: 100%">
								<div>
									<div class="dual-set">
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('maybe')">
											{{ t('maybe') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['maybe']"/>
										</button>
									</div>
								</div>
								<div v-if="isSpaceToAttend || myAttendingStatus['attending']">
									<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('attending')">
											{{ t('I WILL ATTEND') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['attending']"/>
										</button>
									</div>
								</div>
								<div v-else>
									<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('wait_list')">
											{{ t('wait_list') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['wait_list']"/>
										</button>
									</div>
								</div>
								<div>
									<div class="dual-set">
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('decline')">
											{{ t('decline') }}
											<input type="checkbox" class="checkbox" onclick="return false;"/>
										</button>
									</div>
								</div>
							</div>
							<!--if public and not invited, can click maybe / attending-->
							<div style="width: 100%;" v-if="!myAttendingStatus['invited'] && !event.is_private">
								<div>
									<div class="dual-set">
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('maybe')">
											{{ t('maybe') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['maybe']"/>
										</button>
									</div>
								</div>
								<div v-if="isSpaceToAttend">
									<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('attending')">
											{{ t('I WILL ATTEND') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['attending']"/>
										</button>
									</div>
								</div>
								<div v-else>
									<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('wait_list')">
											{{ t('wait_list') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['wait_list']"/>
										</button>
									</div>
								</div>
							</div>
							<!--if private and not invited, can click invite request-->
							<div style="width: 100%;" v-if="!myAttendingStatus['invited'] && event.is_private">
								<div>
									<div class="dual-set">
										<button class="button"
												v-on:click.prevent="changeAttendingStatus('invite_request')">
											{{ t('invite_request') }}
											<input type="checkbox" class="checkbox" v-model="myAttendingStatus['invite_request']"/>
										</button>
									</div>
								</div>
							</div>
							<div v-if="(myAttendingStatus['invited'] || myAttendingStatus['invite_request'])"
									style="width: 100%;">
								<button class="button" v-on:click.prevent="plusOneButton()">
									<div v-if="!plusOneStatus" style="width: 100%; text-align: center;">
										{{ t('ADD A PLUS ONE') }}
									</div>
									<div v-else style="width: 100%; display: flex; flex-direction: row;
											justify-content: space-between; align-items: center;">
										{{plusOneStatus}}
										<input type="checkbox" class="checkbox" checked="checked" onclick="return false;"/>
									</div>
								</button>
							</div>
						</div>
						<div style="width: 35px; align-self: flex-start; margin-top: 3px; flex-shrink: 0;">
							<button style="background: none; border: none"
									v-on:click.prevent="showInformation = 'attendingStatus'">
								<img src="@/assets/iIcon.png" class="icon" style="padding: 3px;" id="events-info"/>
							</button>
						</div>
					</div>
				</div>
				<div v-if="(!event.is_private || myAttendingStatus['invited']) && event.venue_name" class="flex-row"
						style="justify-content: space-between; flex-direction: column">
					<p class="event-attr">
						<small>{{t('VENUE')}}</small>
					</p>
					<p class="address-value" style="margin-bottom: 1em;">
						{{ event.venue_name }}
					</p>
				</div>
				<small class="event-attr">{{t('ADDRESS')}}</small>
				<small class="address-value">{{ event.address }}</small>
				<div class="flex-row" style="justify-content: space-between; max-width: 100%;">
					<button class="button event-page-button" v-on:click.prevent="copyToClipboard()"
							style="align-self: center; width: auto; flex-shrink: 1; font-size: 14px;">
						<small>{{t('COPY ADDRESS')}}</small>
					</button>
					<button class="button google-maps-button" v-on:click.prevent="openInGoogleMaps()"
							style="display: flex; flex-direction: row; justify-content: center; width: 100%;
							flex-shrink: 1; font-size: 14px;">
            			<small>{{t('OPEN IN GOOGLE MAPS')}}</small>
					</button>
				</div>
				<small class="event-attr">{{t('DESCRIPTION')}}</small>
				<div style="align-self: center; overflow-y: scroll; max-height: 105px; height: auto; width: 95%; text-align: center;
						margin-bottom: 0.7em; margin-top: 4px; white-space: pre-line; text-indent: 0 !important; line-height: 20px;"
				>{{ event.description }}</div>
				<small class="event-attr">{{t('PEOPLE')}}</small>
				<div style="margin-bottom: 1em; height: auto; margin-top: 4px; width: 100%;">
					<div style="width: 100%; display: flex; flex-direction: column; align-items: center;">
						<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%;">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('invited') }}
								</div>
								<!--can't see invited people if not invited-->
								<button v-on:click.prevent="showStatus = 'invited'" class="button"
										style="align-self: center; width: 100px;"
										:disabled="!myAttendingStatus['invited'] || people['invited'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['invited'].length }}
										<div v-if="people['invited'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('hosts') }}
								</div>
								<!--everyone can see hosts-->
								<button v-on:click.prevent="showStatus = 'hosts'" class="button"
										style="align-self: center; width: 100px;">
									<div class="flex-row" style="align-self: center">
										{{ people['hosts'].length }}
										<div v-if="people['hosts'].length > 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
						</div>
						<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%;">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('attending') }}
								</div>
								<!--can't see attending people if not invited-->
								<button v-on:click.prevent="showStatus = 'attending'" class="button"
										style="align-self: center; width: 100px;"
										:disabled="!myAttendingStatus['invited'] || people['attending'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['attending'].length }}
										<div v-if="people['attending'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('ATTENDING LIMIT') }}
								</div>
								<!--can't see invited people if not invited-->
								<button class="button" :disabled="true" style="align-self: center; width: 100px;
									justify-content: center;"
										:style="[isSpaceToAttend ? {color: 'green', borderColor: 'green'}
										: {color: 'red', borderColor: 'red'}]">
										<div v-if="event.attending_limit != 999999" class="flex-row" style="align-self: center">
											{{ event.attending_limit }}
											<div v-if="event.attending_limit != 1">
												&nbsp;{{ t('PEOPLE') }}
											</div>
											<div v-else>
												&nbsp;{{ t('PERSON') }}
											</div>
										</div>
										<div v-else>
											{{ t('UNLIMITED') }}
										</div>
								</button>
							</div>
						</div>
						<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%;">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('maybe') }}
								</div>
								<!--can't see maybe people if not invited-->
								<button v-on:click.prevent="showStatus = 'maybe'" class="button"
										style="align-self: center; width: 100px;"
										:disabled="!myAttendingStatus['invited'] || people['maybe'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['maybe'].length }}
										<div v-if="people['maybe'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('wait_list') }}
								</div>
								<!--can't see wait_list people if not host-->
								<button v-on:click.prevent="showStatus = 'wait_list'" class="button"
										style="align-self: center; width: 100px;"
										:disabled="!myAttendingStatus['hosts'] || people['wait_list'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['wait_list'].length }}
										<div v-if="people['wait_list'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
						</div>
						<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%;">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('invite_request') }}
								</div>
								<!--can't see invite_request people if not host-->
								<button v-on:click.prevent="showStatus = 'invite_request'" class="button"
										style="align-self: center; width: 100px;"
										:disabled="!myAttendingStatus['hosts'] || people['invite_request'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['invite_request'].length }}
										<div v-if="people['invite_request'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
						</div>
						<div class="card-shape" style="margin-bottom: 3px; width: 95%; max-width: 95%;"
								v-if="myAttendingStatus['hosts']">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									{{ t('uninvited_followers') }}
								</div>
								<button v-on:click.prevent="showStatus = 'uninvited_followers'" class="button"
										style="align-self: center; width: 100px; min-width: 100px;"
										:disabled="!myAttendingStatus['hosts']
										|| people['uninvited_followers'].length === 0">
									<div class="flex-row"
											style="align-self: center">
										{{ people['uninvited_followers'].length }}
										<div v-if="people['uninvited_followers'].length != 1">
											&nbsp;{{ t('PEOPLE') }}
										</div>
										<div v-else>
											&nbsp;{{ t('PERSON') }}
										</div>
									</div>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="line-height"/>
		</div>
		<modal v-if="showStatus" @closeModals="showStatus = null" ref="showStatus">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						{{ t(showStatus) }}
					</div>
					<x-close-button :closeFunc="() => {$refs.showStatus.closeModals()}" style="align-self: flex-end;"/>
				</div>
				<div style="width: 100%; overflow-y: scroll;">
					<div v-for="person in people[showStatus]" style="width: 100%; border: 2px solid #cae2ff;
							border-radius: 15px;">
						<div style="display: flex; flex-direction: row; justify-content: space-between; width: 100%;">
							<div style="min-height: 30px; display: flex; flex-direction: row;
									justify-content: flex-start; align-items: center; max-width: 100%; min-width: 0;
									flex-shrink: 1; write-space: pre-wrap; overflow-wrap: break-word;
									padding-left: 5px;">
								{{person.display_name}}
							</div>
							<button v-on:click.prevent="messagePerson = person" class="button" style="width: auto;
									border: 2px solid #18002e; background-color: #ffe07a; color: #18002e"
									v-if="((myAttendingStatus['hosts'] || showStatus === 'hosts') && isAuthenticatedUser) && !person.plus_one">
								{{ t('MESSAGE') }}
							</button>
						</div>
						<button v-if="myAttendingStatus['hosts'] && !person.plus_one && isAuthenticatedUser
								&& ['invite_request', 'uninvited_followers'].includes(showStatus)"
								v-on:click.prevent="changeAttendingStatus('invited', person.id)" class="button"
								style="border: 2px solid #18002e; background-color: #ffe07a; color: #18002e">
							{{ t('INVITE!') }}
						</button>
					</div>
				</div>
				<div style="padding-right: 10px; width: 100%; margin-top: 10px;">
				<button v-on:click.prevent="messageAllPeople = true" v-if="myAttendingStatus['hosts']"
						class="button">
					{{ t('MESSAGE ALL') }}
				</button>
				</div>
			</div>
		</modal>
		<modal v-if="messagePerson" @closeModals="messagePerson = null" ref="messagePerson"
				:haveBackground="false">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div style="width: 20px;"/>
					<div style="font-size: 20px; text-align: center;">
						{{ t('MESSAGE') }}<br>{{messagePerson.display_name}}
					</div>
					<x-close-button :closeFunc="() => {$refs.messagePerson.closeModals()}" style="align-self: flex-end;"/>
				</div>
				<textarea :placeholder="t('MESSAGE')" v-model="messageContent" type="text"
						autocapitalize="sentences" style="height: 90px;" autocomplete="off"/>
				<button v-on:click.prevent="message()" class="button">
					<div style="width: 100%; text-align: center;">{{ t('SEND') }}</div>
				</button>
			</div>
		</modal>
		<modal v-if="messageAllPeople" @closeModals="messageAllPeople = false" ref="messageAllPeople"
				:haveBackground="false">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div style="width: 20px;"/>
					<div style="font-size: 20px;">
						{{ t('MESSAGE ALL') }}
					</div>
					<x-close-button :closeFunc="() => {$refs.messageAllPeople.closeModals()}" style="align-self: flex-end;"/>
				</div>
				<textarea :placeholder="t('MESSAGE')" v-model="messageContent" type="text"
						autocapitalize="sentences" style="height: 90px;" autocomplete="off"/>
				<button v-on:click.prevent="messageAll(showStatus)" class="button">
					<div style="width: 100%; text-align: center;">{{ t('SEND') }}</div>
				</button>
			</div>
		</modal>
		<modal v-if="plusOneModal" @closeModals="plusOneModal = false" ref="plusOneModal">
			<div slot="contents" class="modal">
				<x-close-button :closeFunc="() => {$refs.plusOneModal.closeModals()}" style="align-self: flex-end;"/>
				<display-name-input ref="plusOneName" usage="PlusOne"
						:enter="changePlusOne" style="width: 100%;"/>
				<button v-on:click.prevent="changePlusOne()" class="button" style="width: 100%;">
					<p style="width: 100%; text-align: center">{{ t('ADD A PLUS ONE') }}</p>
				</button>
        	</div>
		</modal>
		<information v-if="showInformation" :closeInfo="() => {showInformation=null}" :whichInfo="showInformation"/>
		<flash-modal :text="t('DONE!')" ref="flashDone" :time="1500"/>
		<flash-modal :text="t('CAN\'T CHANGE PAST EVENTS')" ref="flashCantChangePastEvents" :time="1500"/>
    	<flash-modal :text="t('COPIED!')" ref="flashCoppied" :time="1500"/>
		<flash-modal :text="t('SENT!')" ref="flashSent" :time="1500"/>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import tabs from '@/components/tabs.vue'
	import modal from '@/components/modal.vue'
	import displayNameInput from '@/components/displayNameInput.vue'
	import flashModal from '@/components/flashModal.vue'
	import xCloseButton from '@/components/xCloseButton.vue'
	import information from '@/components/information'
	export default {
		name: 'event',
		components: {
			tabs,
			modal,
			displayNameInput,
			flashModal,
			xCloseButton,
			information,
		},
		data () {
			return {
				store: store,
				event: store.events.selected,  // just make sure the key fro this component has event in it
				myAttendingStatus: {
					'hosts': false,
					'invited': false,
					'attending': false,
					'maybe': false,
					'wait_list': false,
					'invite_request': false,
				},
				people: {
					'hosts': [],
					'invited': [],
					'attending': [],
					'maybe': [],
					'wait_list': [],
					'invite_request': [],
					'uninvited_followers': [],
				},
				showStatus: null,
				plusOneStatus: '',
				showHostPanel: false,
				messagePerson: null,
				messageContent: '',
				messageAllPeople: false,
				image: require('@/assets/pexels-photo-event4.jpeg'),
				showInformation: null,
				plusOneModal: false,
			}
		},
		computed: {
			getDate () {
				let date_time = this.event.date_time.split('T')
				let date = date_time[0]
				let time = date_time[1]
				time = time.split(':')
				time = time[0] + ':' + time[1]
				return date + '\xa0\xa0-\xa0\xa0' + time
			},
			isAuthenticatedUser () {
				return f.isAuthenticatedUser
			},
			isSpaceToAttend () {
				if (this.plusOneStatus) {
					return this.people['attending'].length + 2 <= this.event.attending_limit
				} else {
					return this.people['attending'].length + 1 <= this.event.attending_limit
				}
			},
		},
		created () {
			this.store.loading = true
		},
		async mounted () {
			await this.getEventAndMyStatusAndPeople()
			if (this.event.image_data) {
				this.image = this.event.image_data
			}
		},
		methods: {
			t (w) { return translations.t(w) },
			goToLogin () {
				f.goToPage({ page: 'loginRegister', args: {} })
			},
			async getEventAndMyStatusAndPeople () {
				this.store.loading = true
				this.event = f.filterEvents(this.store.events.all, f.currentPage.args.id, ['id'], true)[0]
				this.store.events.selected = this.event

				let result = await f.getEventUserInfoCheckPeopleList(this.event.id)
				this.myAttendingStatus = result.myAttendingStatus
				this.people = result.people

				this.plusOneStatus = null
				let keys = Object.keys(this.myAttendingStatus)
				for (let i = 0; i < keys.length; i++) {
					if (this.myAttendingStatus[keys[i]]) {
						for (let j = 0; j < this.people[keys[i]].length; j++) {
							if (this.people[keys[i]][j].id === this.store.user.id && this.people[keys[i]][j].plus_one) {
								this.plusOneStatus = this.people[keys[i]][j].display_name
							}
						}
					}
				}
				this.store.loading = false
			},
			async changeAttendingStatus (status, userId = null) {
				if (!this.isAuthenticatedUser) {
					this.goToLogin()
					return
				}
				if (status === 'invited') {
					store.loading = true
					let result = await api.changeGuestStatus(this.event.id, status, userId)
					if (result === 'failed') {
						store.loading = false
						await this.$refs.flashCantChangePastEvents.flashModal()
						return
					}
					await f.getEvent(this.event)
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
					await this.$refs.flashDone.flashModal()
					return
				} else if (status === 'decline' || !this.myAttendingStatus[status]) {
					store.loading = true
					let result = await api.changeGuestStatus(this.event.id, status, null)
					if (result === 'failed') {
						store.loading = false
						await this.$refs.flashCantChangePastEvents.flashModal()
						return
					}
					await f.getEvent(this.event)
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
					await this.$refs.flashDone.flashModal()
					return
				} else if (status === 'invite_request') {
					// if my status is already this status, only change it if im changing invite_request
					store.loading = true
					let result = await api.changeGuestStatus(this.event.id, 'decline', null)
					if (result === 'failed') {
						store.loading = false
						await this.$refs.flashCantChangePastEvents.flashModal()
						return
					}
					await f.getEvent(this.event)
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
					await this.$refs.flashDone.flashModal()
					return
				}  // otherwise, if my status is already this status, do nothing
			},
			async plusOneButton () {
				if (this.plusOneStatus) {  // already has plus one
					this.store.loading = true
					let result = await api.deletePlusOne(this.event.id)
					if (result === 'failed') {
						store.loading = false
						await this.$refs.flashCantChangePastEvents.flashModal()
						return
					}
					await f.getEvent(this.event)
					await this.getEventAndMyStatusAndPeople()
					this.store.loading = false
					await this.$refs.flashDone.flashModal()
					return
				} else {
					this.plusOneModal = true
				}
			},
			async changePlusOne () {
				this.$refs.plusOneName.hasErrors()
				if (this.$refs.plusOneName.error.length > 0) {
					f.shakeFunction([this.$refs.plusOneName])
					return
				}
				this.store.loading = true
				let result = await api.setPlusOne(this.event.id, this.$refs.plusOneName.displayName)
				if (result === 'failed') {
					store.loading = false
					await this.$refs.flashCantChangePastEvents.flashModal()
					return
				}
				await f.getEvent(this.event)
				await this.getEventAndMyStatusAndPeople()
				this.$refs.plusOneModal.closeModals()
				this.store.loading = false
				await this.$refs.flashDone.flashModal()
				return
			},
			openInGoogleMaps () {
				window.open('http://maps.google.com/?q=' + this.event.address,'_blank')
			},
			async message () {
				this.store.loading = true
				await api.messageUser(this.event.id, this.messagePerson.id, this.messageContent)
				this.messagePerson = null
				this.messageContent = ''
				this.store.loading = false
				await this.$refs.flashSent.flashModal()
			},
			async messageAll (guestStatus) {
				this.store.loading = true
				let ids = []
				for (let i = 0; i < this.people[guestStatus].length; i++) {
					if (!this.people[guestStatus][i]['plus_one']) {
						ids.push(this.people[guestStatus][i]['id'])
					}
				}
				await api.messageUsers(this.event.id, ids, this.messageContent)
				this.messageAllPeople = false
				this.messageContent = ''
				this.store.loading = false
				await this.$refs.flashSent.flashModal()
			},
      	async copyToClipboard () {
				navigator.clipboard.writeText(this.event.address)
				//// if the above fails on some browser, this is supposed to work. maybe use both if the first fails
				//let textArea = document.createElement("textarea")
				//textArea.value = this.url
				//textArea.hidden = true  // not sure about this line or not
				//document.body.appendChild(textArea)
				//textArea.select()
				//document.execCommand('copy')

				await this.$refs.flashCoppied.flashModal()
			}
			//// do not delete, this will be used soon. and it took forever to get this shit to work
			//async getEventImage () {
			//	let result = await api.getEventImage(this.getimgid, eventId) // this.event.id
			//	this.imagetwo = "data:image/jpg;base64," + result['image_data']
			//},
		} // methods
	} // export
</script>
<style scoped>
	.flex-table {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.flex-row {
		width: 95%;
		display: flex;
		flex-direction: row;
		justify-content: center;
	}
	.dual-set {
		display: flex;
		flex-direction: row;
		align-self: center;
		align-items: center;
		justify-content: center;
		padding: 0;
		width: 100%;
	}
	.checkbox {
		height: 20px;
		width: 20px;
		z-index: 1;
		flex-shrink: 0;
	}
	.button {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}
	.tabs {
		border: none;
	}
	.event-page-button{
		align-self: center;
		/* white-space: pre-line; */
		height: auto;
		min-height: 30px;
		margin-bottom: 1em;
	}
	.drop-down-button {
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
		width: 100%;
	}
	.google-maps-button {
		align-self: center;
		height: auto;
		min-height: 30px;
		margin-bottom: 1em;
		background-color:#ffe07a;
		color: black;
	}
	.address-value {
		margin: 0 auto;
		text-align: center;
		margin-top: 3px;
	}
	.event-attr {
		border-bottom: solid 1px;
		width: 70%;
		margin-bottom: 2px;
		text-align: center;
		margin: 0 auto;
	}
</style>
