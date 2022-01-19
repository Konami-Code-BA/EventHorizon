<template>
	<div class="main" v-if="store.events.selected">
		<div class="flex-row" style="align-items: center; justify-content: center; height: 60px;">
			<h2 style="max-width: 80%; overflow-x: scroll;">{{event.name}}</h2>
		</div>
		<div class="flex-row" style="justify-content: space-between">
			<div>
				{{ getDate }}
			</div>
			<div>
				<small>{{ event.is_private ? 'PRIVATE EVENT' : 'PUBLIC EVENT' }}</small>
			</div>
		</div>
		<br>
		<div v-if="attendingStatus['invited'] || !event.is_private"
				style="width: 100%; display: flex; flex-direction: column; align-items: center;">
			<div class="dual-set" v-if="attendingStatus['invited']">
				YOU ARE INVITED
				<input type="checkbox" class="checkbox" checked="checked" onclick="return false;"/>
			</div>
			<tabs :num-tabs="3" :initial="0" style="width: 100%;">
				<div slot="1">
					<div class="dual-set">
						<button class="button" style="width: auto"
								v-on:click.prevent="changeAttendingStatus('maybe')">
							MAYBE
							<input type="checkbox" class="checkbox" v-model="attendingStatus['maybe']"/>
						</button>
					</div>
				</div>
				<div slot="2">
					<div class="dual-set"><!--if limit is not surpassed, otherwise show a waitlist option-->
						<button class="button" style="width: auto"
								v-on:click.prevent="changeAttendingStatus('attending')">
							I WILL ATTEND
							<input type="checkbox" class="checkbox" v-model="attendingStatus['attending']"/>
						</button>
					</div>
				</div>
				<div slot="3">
					<div class="dual-set">
						<button class="button" style="width: auto"
								v-on:click.prevent="changeAttendingStatus('decline')">
							DECLINE
						</button>
					</div>
				</div>
			</tabs>
		</div>
		<div class="flex-table">
			<div style="align-self: center">
				{{ event.description }}
			</div>
			<div v-if="(!event.is_private || attendingStatus['invited']) && event.venue_name" class="flex-table">
				<br>
				<div>
					VENUE:
				</div>
				<div style="align-self: center">
					{{ event.venue_name }}
				</div>
			</div>
			<br>
			<div style="align-self: center">
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<small>{{ event.address }}</small>
				</button>
			</div>
			<br>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					HOSTS
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"><!--everyone can see hosts-->
					<div class="flex-row" style="align-self: center"><!--everyone can see hosts-->
						{{ event.hosts.length }}
						<div v-if="event.hosts.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					INVITED
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!attendingStatus['invited'] && event.is_private">
					<div v-if="attendingStatus['invited'] || !event.is_private" class="flex-row"
							style="align-self: center">
						{{ event.invited.length }}
						<div v-if="Array.isArray(event.invited)">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.invited }}
						<div v-if="Array.isArray(event.invited)">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					ATTENDING
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!attendingStatus['invited'] && event.is_private">
					<div v-if="attendingStatus['invited'] || !event.is_private" class="flex-row"
							style="align-self: center">
						{{ event.attending.length }}
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.attending }}
					</div>
					<div v-if="Array.isArray(event.attending)">
						&nbsp;people
					</div>
					<div v-else>
						&nbsp;person
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					MAYBE
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!attendingStatus['invited'] && event.is_private">
					<div v-if="attendingStatus['invited'] || !event.is_private" class="flex-row"
							style="align-self: center">
						{{ event.maybe.length }}
						<div v-if="0 >= event.maybe.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.maybe }}
						<div v-if="event.maybe > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	import tabs from '@/components/tabs.vue'
	export default {
		name: 'event',
		components: {
			tabs,
		},
		data () {
			return {
				store: store,
				event: store.events.selected,  // just make sure the key fro this component has event in it
				attendingStatus: {
					'host': false,
					'invited': false,
					'attending': false,
					'maybe': false,
					'waitList': false,
					'inviteRequest': false,
				},
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
		},
		mounted () {
			// we start with an id in args and get this event. save to this.event, and then save to store
			this.event = f.filterEvents(this.store.events.all, f.currentPage.args.id, ['id'], true)[0]
			this.store.events.selected = this.event
			this.attendingStatus['hosts'] = f.isGuestStatus(this.event, 'hosts')
			this.attendingStatus['invited'] = f.isGuestStatus(this.event, 'invited')
			this.attendingStatus['attending'] = f.isGuestStatus(this.event, 'attending')
			this.attendingStatus['maybe'] = f.isGuestStatus(this.event, 'maybe')
			this.attendingStatus['wait_list'] = f.isGuestStatus(this.event, 'wait_list')
			this.attendingStatus['invite_request'] = f.isGuestStatus(this.event, 'invite_request')
		},
		methods: {
			t (w) { return translations.t(w) },
			async changeAttendingStatus (status) {
				store.loading = true
				await api.changeGuestStatus(this.event.id, status, null)
				await f.getEvents()
				this.event = f.filterEvents(this.store.events.all, f.currentPage.args.id, ['id'], true)[0]
				this.store.events.selected = this.event
				this.attendingStatus['hosts'] = f.isGuestStatus(this.event, 'hosts')
				this.attendingStatus['invited'] = f.isGuestStatus(this.event, 'invited')
				this.attendingStatus['attending'] = f.isGuestStatus(this.event, 'attending')
				this.attendingStatus['maybe'] = f.isGuestStatus(this.event, 'maybe')
				this.attendingStatus['wait_list'] = f.isGuestStatus(this.event, 'wait_list')
				this.attendingStatus['invite_request'] = f.isGuestStatus(this.event, 'invite_request')
				store.loading = false
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
</style>
