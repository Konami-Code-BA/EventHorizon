<template>
	<div class="main" v-if="store.events.selected && event" style="overflow-y: scroll">
		<div style="width: 98%; display: flex; flex-direction: column; align-items: center; height: auto;">
			<div class="flex-row" style="align-items: center; justify-content: center; height: 60px;">
				<h2 style="max-width: 80%; overflow-x: scroll; max-height: 100%; overflow-y: hidden;
						white-space: nowrap">
					{{event.name}}
				</h2>
			</div>
			<div class="flex-row" style="justify-content: space-between;">
				<div>
					{{ getDate }}
				</div>
				<div>
					<small>{{ event.is_private ? 'PRIVATE EVENT' : 'PUBLIC EVENT' }}</small>
				</div>
			</div>
			<img :src="image" style="height: 160px; width: auto; margin-top: 16px; margin-bottom: 10px; border-radius: 2px;"/>
			<div class="flex-table" style="height: auto;">
				<!-- <br v-if="(!event.is_private || myAttendingStatus['invited']) && event.venue_name"/> -->
				<div v-if="(!event.is_private || myAttendingStatus['invited']) && event.venue_name" class="flex-row"
						style="justify-content: space-between; flex-direction: column">
					<p class="event-attr">
						<strong>Venue</strong>
					</p>
					<p class="address-value" style="margin-bottom: 1em;">
						{{ event.venue_name }}
					</p>
				</div>
					<small class="event-attr">Address</small>
					<small class="address-value">{{ event.address }}</small>
				<div class="flex-row" style="justify-content: space-between;">
					<button class="button event-page-button" v-on:click.prevent="copyToClipboard()"
							style="align-self: center; width: auto;">
						<small> Copy Address </small>
					</button>
					<button class="button google-maps-button" v-on:click.prevent="openInGoogleMaps()"
							style="display: flex; flex-direction: row; justify-content: center; width: 100%;">
            			Open in Google Maps
					</button>
				</div>
				<button v-on:click.prevent="showDescription=!showDescription" class="button event-page-button">
					<div v-if="!showDescription" class="drop-down-button">
						<div style="width: 10px;"/>
						<div>{{ t('SHOW DESCRIPTION') }}</div>
						<div style="width: 10px;">⇩</div>
					</div>
					<div v-else class="drop-down-button">
						<div style="width: 10px;"/>
						<div>{{ t('HIDE DESCRIPTION') }}</div>
						<div style="width: 10px;">⇧</div>
					</div>
				</button>
				<div style="align-self: center; overflow-y: scroll; max-height: 100px; height: auto; margin-bottom: 0.7em" v-show="showDescription">
					{{ event.description }}
				</div>
				<button v-on:click.prevent="showPeople=!showPeople" class="button event-page-button" style="align-self: center">
					<div v-if="!showPeople" class="drop-down-button">
						<div style="width: 10px;"/>
						<div>	{{ t('SHOW PEOPLE') }}</div>
						<div style="width: 10px;">⇩</div>
					</div>
					<div v-else class="drop-down-button">
						<div style="width: 10px;"/>
						<div>{{ t('HIDE PEOPLE') }}</div>
						<div style="width: 10px;">⇧</div>
					</div>
				</button>
				<div v-show="showPeople" style="margin-bottom: 1em; height: auto;">
					<div>
						<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
								padding: 5px; width: 100%;">
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
						<div style="border: 2px solid rgba(255, 255, 255, .3); border-radius: 7px; padding: 5px; width: 100%;">
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
						<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
								padding: 5px; width: 100%;">
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
						<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
								padding: 5px; width: 100%;">
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
						<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
								padding: 5px; width: 100%;" v-if="myAttendingStatus['hosts']">
							<div class="flex-row" style="justify-content: space-between">
								<div style="align-self: center">
									TOTAL UNINVITED FOLLOWERS
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
			<!-- <br> -->
			<button v-on:click.prevent="showEventStatus=!showEventStatus" class="button" style="align-self: center">
					<div v-if="!showEventStatus" class="drop-down-button">
						<div style="width: 10px;"/>
						<div v-if="myAttendingStatus['invited']">SHOW ATTENDING STATUS</div>
						<div v-else>{{ t('CLICK TO JOIN') }}</div>
						<div style="width: 10px;">⇩</div>
					</div>
					<div v-else class="drop-down-button">
						<div style="width: 10px;"/>
						<div>{{ t('HIDE ATTENDING STATUS') }}</div>
						<div style="width: 10px;">⇧</div>
					</div>
			</button>
			<div v-show="!isSpaceToAttend && showEventStatus" style="color: red; width: 100%; text-align: center;">
				THE EVENT IS FULL
			</div>
			<div style="margin-top: 0.7em; width: 100%; display: flex; flex-direction: column; align-items: center;
					border: 2px solid rgba(255, 255, 255, .3); border-radius: 7px;" v-show="showEventStatus">
				<div class="dual-set" v-if="myAttendingStatus['invited']"
						style="border-bottom: 2px solid rgba(255, 255, 255, .3); width: 80%; margin-bottom: 5px;">
					{{ t('invited') }}
					<input type="checkbox" class="checkbox" checked="checked" onclick="return false;"/>
				</div>
				<!--if invited, can click maybe / attending / decline-->
				<div v-if="myAttendingStatus['invited']" style="width: 70%">
					<div>
						<div class="dual-set">
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('maybe')">
								{{ t('MAYBE') }}
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
								{{ t('DECLINE') }}
								<input type="checkbox" class="checkbox" onclick="return false;"/>
							</button>
						</div>
					</div>
				</div>
				<!--if public and not invited, can click maybe / attending-->
				<div style="width: 70%;" v-if="!myAttendingStatus['invited'] && !event.is_private">
					<div>
						<div class="dual-set">
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('maybe')">
								MAYBE
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['maybe']"/>
							</button>
						</div>
					</div>
					<div v-if="isSpaceToAttend">
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('attending')">
								I WILL ATTEND
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['attending']"/>
							</button>
						</div>
					</div>
					<div v-else>
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('wait_list')">
								WAIT LIST
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['wait_list']"/>
							</button>
						</div>
					</div>
				</div>
				<!--if private and not invited, can click invite request-->
				<div style="width: 70%;" v-if="!myAttendingStatus['invited'] && event.is_private">
					<div>
						<div class="dual-set">
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('invite_request')">
								INVITE REQUEST
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['invite_request']"/>
							</button>
						</div>
					</div>
				</div>
				<div v-if="(myAttendingStatus['invited'] || myAttendingStatus['invite_request'])"
						style="display: flex; flex-direction: row; align-items: flex-start; width: 95%;
						padding-top: 5px;">
					<div class="dual-set" style="padding-bottom: 2px; width: auto; align-self: flex-start">
						<button class="button" v-on:click.prevent="changePlusOne()">
							ADD A PLUS ONE
							&nbsp;
							<input type="checkbox" class="checkbox" v-model="plusOneStatus" :key="plusOneStatus"/>
							<!--need to check if i have plus one and put in checkbox and show name instead of input-->
						</button>
					</div>
					<display-name-input ref="displayNameInput" usage="PlusOne"
							v-if="!plusOneStatus" style="width: 50%;" :enter="changePlusOne"/>
					<div v-else style="width: 50%; align-self: center; text-align: center">
						Plus One: {{plusOneStatus.slice(5)}}
					</div>
				</div>
				<!--button v-on:click.prevent="showHostPanel = true" v-if="myAttendingStatus['hosts']" class="button">
					OPEN HOST PANEL
				</button-->
			</div>
			<div class="line-height"/>
		</div>
		<modal v-if="showStatus" @closeModals="showStatus = null">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						{{ t(showStatus) }}
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="showStatus = null" class="no-border-button x-button">
							✖
						</button>
					</div>
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
								MESSAGE
							</button>
						</div>
						<button v-if="myAttendingStatus['hosts'] && !person.plus_one && isAuthenticatedUser
								&& ['invite_request', 'uninvited_followers'].includes(showStatus)"
								v-on:click.prevent="changeAttendingStatus('invited', person.id)" class="button"
								style="border: 2px solid #18002e; background-color: #ffe07a; color: #18002e">
							INVITE!
						</button>
					</div>
				</div>
				<div style="padding-right: 10px; width: 100%; margin-top: 10px;">
				<button v-on:click.prevent="messageAllPeople = true" v-if="myAttendingStatus['hosts']"
						class="button">
					MESSAGE ALL
				</button>
				</div>
			</div>
		</modal>
		<!--modal v-if="showHostPanel" @closeModals="showHostPanel = false">
			<div slot="contents" class="modal" style="max-height: 50%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						HOST PANEL
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="showHostPanel = false" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<button v-on:click.prevent="showHostPanel = true" v-if="myAttendingStatus['hosts']" class="button">
					MESSAGE ALL
				</button>
			</div>
		</modal-->
		<modal v-if="messagePerson" @closeModals="messagePerson = null">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div style="width: 20px;"/>
					<div style="font-size: 24px; text-align: center;">
						MESSAGE<br>{{messagePerson.display_name}}
					</div>
					<div style="padding-bottom: 5px; width: 20px;">
						<button v-on:click.prevent="messagePerson = null" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<textarea placeholder="MESSAGE" v-model="messageContent" type="text"
						autocapitalize="sentences" style="height: 90px;" autocomplete="off"/>
				<button v-on:click.prevent="message()" class="button">
					SEND
				</button>
			</div>
		</modal>
		<modal v-if="messageAllPeople" @closeModals="messageAllPeople = false">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div style="width: 20px;"/>
					<div style="font-size: 24px;">
						MESSAGE ALL
					</div>
					<div style="padding-bottom: 5px; width: 20px;">
						<button v-on:click.prevent="messageAllPeople = false" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<textarea placeholder="MESSAGE" v-model="messageContent" type="text"
						autocapitalize="sentences" style="height: 90px;" autocomplete="off"/>
				<button v-on:click.prevent="messageAll(showStatus)" class="button">
					SEND
				</button>
			</div>
		</modal>
		<flash-modal :text="t('DONE!')" ref="flashDone" :time="1500"/>
		<flash-modal :text="'CAN\'T CHANGE PAST EVENTS'" ref="flashCantChangePastEvents" :time="1500"/>
    <flash-modal :text="'Copied!'" ref="flashCoppied" :time="1500"/>
		<flash-modal :text="'SENT!'" ref="flashSent" :time="1500"/>
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
	export default {
		name: 'event',
		components: {
			tabs,
			modal,
			displayNameInput,
			flashModal,
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
				plusOneStatus: null,
				showHostPanel: false,
				messagePerson: null,
				messageContent: '',
				messageAllPeople: false,
				showPeople: false,
				image: require('@/assets/pexels-photo-event4.jpeg'),
				showDescription: false,
				showEventStatus: false,
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
			async changePlusOne () {
				if (this.plusOneStatus) {
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
					this.$refs.displayNameInput.hasErrors()
					if (this.$refs.displayNameInput.error.length > 0) {
						f.shakeFunction([this.$refs.displayNameInput])
						return
					}
					this.store.loading = true
					let result = await api.setPlusOne(this.event.id, this.$refs.displayNameInput.displayName)
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
				}
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
	}
	.flex-row {
		width: 100%;
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
	}
	.checkbox {
		height: 20px;
		width: 20px;
		z-index: 1;
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
	}
	.event-attr {
		border-bottom: solid 1px;
		width: 70%;
		margin-bottom: 2px;
		text-align: center;
		margin: 0 auto;
	}
</style>
