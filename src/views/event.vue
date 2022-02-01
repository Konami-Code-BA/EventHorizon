<template>
	<div class="main" v-if="store.events.selected && !store.loading" style="overflow-y: scroll">
		<div style="width: 98%;">
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
			<br>
			<div class="flex-table">
				<div style="align-self: center; overflow-y: scroll; height: 100px;">
					{{ event.description }}
				</div>
				<br v-if="(!event.is_private || myAttendingStatus['invited']) && event.venue_name"/>
				<div v-if="(!event.is_private || myAttendingStatus['invited']) && event.venue_name" class="flex-row"
						style="justify-content: space-between;">
					<div>
						VENUE :
					</div>
					<div>
						{{ event.venue_name }}
					</div>
				</div>
				<br>
				<div style="align-self: center; width: 100%;">
					<button v-on:click.prevent="openInGoogleMaps()" class="button"
							style="align-self: center; white-space: pre-line; height: auto;">
						<small>{{ event.address }}</small>
					</button>
				</div>
				<br>
				<button v-on:click.prevent="showPeople = true" class="button" style="align-self: center">
					SHOW PEOPLE
				</button>
			</div>
			<br>
			<div v-if="!isSpaceToAttend" style="color: red; width: 100%; text-align: center;">
				THE EVENT IS FULL
			</div>
			<br>
			<div style="width: 100%; display: flex; flex-direction: column; align-items: center;
					border: 2px solid rgba(255, 255, 255, .3); border-radius: 7px;">
				<div class="dual-set" v-if="myAttendingStatus['invited']" style="border-bottom: 2px solid rgba(255, 255, 255, .3)">
					YOU ARE INVITED
					<input type="checkbox" class="checkbox" checked="checked" onclick="return false;"/>
				</div>
				<!--if invited, can click maybe / attending / decline-->
				<tabs :num-tabs="3" :initial="0"
						v-if="myAttendingStatus['invited']">
					<div slot="1">
						<div class="dual-set">
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('maybe')">
								MAYBE
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['maybe']"/>
							</button>
						</div>
					</div>
					<div slot="2" v-if="isSpaceToAttend || myAttendingStatus['attending']">
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('attending')">
								I WILL ATTEND
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['attending']"/>
							</button>
						</div>
					</div>
					<div slot="2" v-else>
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('wait_list')">
								WAIT LIST
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['wait_list']"/>
							</button>
						</div>
					</div>
					<div slot="3">
						<div class="dual-set">
							<button class="button"
									v-on:click.prevent="changeAttendingStatus('decline')">
								DECLINE
							</button>
						</div>
					</div>
				</tabs>
				<!--if public and not invited, can click maybe / attending-->
				<tabs :num-tabs="2" :initial="0" style="width: 100%;"
						v-if="!myAttendingStatus['invited'] && !event.is_private">
					<div slot="1">
						<div class="dual-set">
							<button class="button" style="width: auto"
									v-on:click.prevent="changeAttendingStatus('maybe')">
								MAYBE
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['maybe']"/>
							</button>
						</div>
					</div>
					<div slot="2" v-if="isSpaceToAttend">
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button" style="width: auto"
									v-on:click.prevent="changeAttendingStatus('attending')">
								I WILL ATTEND
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['attending']"/>
							</button>
						</div>
					</div>
					<div slot="2" v-else>
						<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
							<button class="button" style="width: auto"
									v-on:click.prevent="changeAttendingStatus('wait_list')">
								WAIT LIST
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['wait_list']"/>
							</button>
						</div>
					</div>
				</tabs>
				<!--if private and not invited, can click invite request-->
				<tabs :num-tabs="1" :initial="0" style="width: 100%;"
						v-if="!myAttendingStatus['invited'] && event.is_private">
					<div slot="1">
						<div class="dual-set">
							<button class="button" style="width: auto"
									v-on:click.prevent="changeAttendingStatus('invite_request')">
								INVITE REQUEST
								<input type="checkbox" class="checkbox" v-model="myAttendingStatus['invite_request']"/>
							</button>
						</div>
					</div>
				</tabs>
				<div class="line-height" v-if="(myAttendingStatus['invited'] || myAttendingStatus['invite_request'])"/>
				<div v-if="(myAttendingStatus['invited'] || myAttendingStatus['invite_request'])"
						style="display: flex; flex-direction: row; align-items: flex-start; width: 100%;">
					<display-name-input ref="displayNameInput" usage="PlusOne" :dontStartError="true"
							v-if="!plusOneStatus" style="width: 50%;" :enter="changePlusOne"/>
					<div v-else style="width: 50%;">Plus One: {{plusOneStatus.slice(5)}}</div>
					<div class="dual-set" style="padding-bottom: 2px; width: auto; align-self: flex-start">
						<button class="button" v-on:click.prevent="changePlusOne()">
							ADD A PLUS ONE
							&nbsp;
							<input type="checkbox" class="checkbox" v-model="plusOneStatus" :key="plusOneStatus"/>  <!--need to check if i have plus one and put in checkbox and show name instead of input-->
						</button>
					</div>
				</div>
				<!--button v-on:click.prevent="showHostPanel = true" v-if="myAttendingStatus['hosts']" class="button">
					OPEN HOST PANEL
				</button-->
			</div>
		</div>
		<modal v-if="showPeople" @closeModals="showPeople = false">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						PEOPLE
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="showPeople = false" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
						padding: 5px; width: 100%;">
					<div class="flex-row" style="justify-content: space-between">
						<div style="align-self: center">
							{{ t('TOTAL INVITED') }}
						</div>
						<!--can't see invited people if not invited-->
						<button v-on:click.prevent="showStatus = 'invited'; showPeople = false" class="button"
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
							{{ t('HOSTS') }}
						</div>
						<!--everyone can see hosts-->
						<button v-on:click.prevent="showStatus = 'hosts'; showPeople = false" class="button"
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
							{{ t('ATTENDING') }}
						</div>
						<!--can't see attending people if not invited-->
						<button v-on:click.prevent="showStatus = 'attending'; showPeople = false" class="button"
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
							ATTENDING LIMIT
						</div>
						<!--can't see invited people if not invited-->
						<button class="button" :disabled="true" style="align-self: center; width: 100px;"
								:style="[isSpaceToAttend ? {color: 'green', borderColor: 'green'}
								: {color: 'red', borderColor: 'red'}]">
							<div>
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
									UNLIMITED
								</div>
							</div>
						</button>
					</div>
				</div>
				<div style="border: 2px solid rgba(255, 255, 255, .3); margin-bottom: 3px; border-radius: 7px;
						padding: 5px; width: 100%;">
					<div class="flex-row" style="justify-content: space-between">
						<div style="align-self: center">
							{{ t('MAYBE') }}
						</div>
						<!--can't see maybe people if not invited-->
						<button v-on:click.prevent="showStatus = 'maybe'; showPeople = false" class="button"
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
							{{ t('WAIT LIST') }}
						</div>
						<!--can't see wait_list people if not host-->
						<button v-on:click.prevent="showStatus = 'wait_list'; showPeople = false" class="button"
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
							{{ t('INVITE REQUESTS') }}
						</div>
						<!--can't see invite_request people if not host-->
						<button v-on:click.prevent="showStatus = 'invite_request'; showPeople = false" class="button"
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
			</div>
		</modal>
		<modal v-if="showStatus" @closeModals="showStatus = null">
			<div slot="contents" class="modal" style="height: 55%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						{{ statusNames[showStatus] }}
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="showPeople = true; showStatus = null" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<div style="width: 100%; overflow-y: scroll;">
					<div v-for="person in people[showStatus]">
						<div style="display: flex; flex-direction: row;
								justify-content: space-between;">
							<div style="height: 30px; display: flex; flex-direction: column; justify-content: center;">
								●　{{person.display_name}}
							</div>
							<button v-on:click.prevent="messagePerson = person" class="button" style="width: 50px;"
									v-if="(myAttendingStatus['hosts'] || showStatus === 'hosts') && !person.plus_one">
								MSG
							</button>
						</div>
					</div>
				</div>
				<button v-on:click.prevent="messageAllPeople = true" v-if="myAttendingStatus['hosts']"
						class="button">
					MESSAGE ALL
				</button>
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
			<div slot="contents" class="modal" style="max-height: 50%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						MESSAGE
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="messagePerson = null" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<input v-model="messageContent" type="text"/>
				<button v-on:click.prevent="message()" class="button">
					SEND
				</button>
			</div>
		</modal>
		<modal v-if="messageAllPeople" @closeModals="messageAllPeople = false">
			<div slot="contents" class="modal" style="max-height: 50%;">
				<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;
						align-content: flex-start">
					<div/>
					<div style="font-size: 24px;">
						MESSAGE
					</div>
					<div style="padding-bottom: 5px;">
						<button v-on:click.prevent="messageAllPeople = false" class="no-border-button x-button">
							✖
						</button>
					</div>
				</div>
				<input v-model="messageContent" type="text"/>
				<button v-on:click.prevent="messageAll(showStatus)" class="button">
					SEND
				</button>
			</div>
		</modal>
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
	export default {
		name: 'event',
		components: {
			tabs,
			modal,
			displayNameInput,
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
				},
				showStatus: null,
				statusNames: {
					'hosts': this.t('HOSTS'),
					'invited': this.t('TOTAL INVITED'),
					'attending': this.t('ATTENDING'),
					'maybe': this.t('MAYBE'),
					'wait_list': this.t('WAIT LIST'),
					'invite_request': this.t('INVITE REQUESTS'),
				},
				plusOneStatus: null,
				showHostPanel: false,
				messagePerson: null,
				messageContent: '',
				messageAllPeople: false,
				showPeople: false,
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

				this.people['hosts'] = await api.getEventUserInfo(this.event.id, 'hosts')
				this.people['invited'] = await api.getEventUserInfo(this.event.id, 'invited')
				this.people['maybe'] = await api.getEventUserInfo(this.event.id, 'maybe')
				this.people['attending'] = await api.getEventUserInfo(this.event.id, 'attending')
				this.people['wait_list'] = await api.getEventUserInfo(this.event.id, 'wait_list')
				this.people['invite_request'] = await api.getEventUserInfo(this.event.id, 'invite_request')

				this.myAttendingStatus['hosts'] = this.checkPeopleList('hosts')
				this.myAttendingStatus['invited'] = this.checkPeopleList('invited')
				this.myAttendingStatus['attending'] = this.checkPeopleList('attending')
				this.myAttendingStatus['maybe'] = this.checkPeopleList('maybe')
				this.myAttendingStatus['wait_list'] = this.checkPeopleList('wait_list')
				this.myAttendingStatus['invite_request'] = this.checkPeopleList('invite_request')

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
			checkPeopleList (guestStatus) {
				let me = {
					id: this.store.user.id,
					display_name: this.store.user.display_name,
					limited_user: true,
					plus_one: false,
				}
				for (let i = 0; i < this.people[guestStatus].length; i++ ) {
					if (JSON.stringify(this.people[guestStatus][i]) === JSON.stringify(me)) {
						return true
					}
				}
				return false
			},
			async changeAttendingStatus (status) {
				if (!this.isAuthenticatedUser) {
					this.goToLogin()
					return
				}
				if (status === 'decline' || !this.myAttendingStatus[status]) {
					store.loading = true
					await api.changeGuestStatus(this.event.id, status, null)
					await f.getEvents()
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
				} else if (status === 'invite_request') {
					// if my status is already this status, only change it if im changing invite_request
					store.loading = true
					await api.changeGuestStatus(this.event.id, 'decline', null)
					await f.getEvents()
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
				}  // otherwise, if my status is already this status, do nothing
			},
			async changePlusOne () {
				if (this.plusOneStatus) {
					store.loading = true
					await api.deletePlusOne(this.event.id)
					await f.getEvents()
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
				} else {
					if (this.$refs.displayNameInput.displayName === '') {
						this.$refs.displayNameInput.error = 'Required'
					}
					if (this.$refs.displayNameInput.error.length > 0) {
						f.shakeFunction([this.$refs.displayNameInput])
						return
					}
					store.loading = true
					await api.setPlusOne(this.event.id, this.$refs.displayNameInput.displayName)
					await f.getEvents()
					await this.getEventAndMyStatusAndPeople()
					store.loading = false
				}
			},
			openInGoogleMaps () {
				window.open('http://maps.google.com/?q=' + this.event.address,'_blank')
			},
			async message () {
				await api.messageUser(this.event.id, this.messagePerson.id, this.messageContent)
				this.messagePerson = null
			},
			async messageAll (guestStatus) {
				let ids = []
				for (let i = 0; i < this.people[guestStatus].length; i++) {
					if (!this.people[guestStatus][i]['plus_one']) {
						ids.push(this.people[guestStatus][i]['id'])
					}
				}
				await api.messageUsers(this.event.id, ids, this.messageContent)
				this.messageAllPeople = false
			},
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
	}
	.tabs {
		border: none;
	}
</style>
